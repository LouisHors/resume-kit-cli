import html
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .errors import ResumeKitError
from .renderers import formalize_publish_resume_text, strip_manual_review_section


def export_resume_markdown(markdown_path, html_path=None, pdf_path=None, force=False):
    if html_path is None and pdf_path is None:
        raise ResumeKitError("At least one export target is required", {"targets": ["html", "pdf"]})

    markdown_path = Path(markdown_path)
    source_text = markdown_path.read_text(encoding="utf-8")
    publish_text = formalize_publish_resume_text(source_text)
    html_text = render_resume_html(publish_text)
    written = []

    html_out = Path(html_path) if html_path is not None else None
    pdf_out = Path(pdf_path) if pdf_path is not None else None
    for target in [path for path in (html_out, pdf_out) if path is not None]:
        if target.exists():
            if not force:
                raise ResumeKitError("Output file already exists", {"path": str(target)})
            target.unlink()

    if html_out is not None:
        html_out.parent.mkdir(parents=True, exist_ok=True)
        html_out.write_text(html_text, encoding="utf-8")
        written.append(html_out)

    if pdf_out is not None:
        with tempfile.TemporaryDirectory(prefix="resume-kit-export-") as tempdir:
            html_source = Path(tempdir) / "resume.html"
            html_source.write_text(html_text, encoding="utf-8")
            _write_pdf_from_html(html_source, pdf_out)
        written.append(pdf_out)

    return written


def render_resume_html(markdown_text):
    body, title = _markdown_to_html_body(markdown_text)
    escaped_title = html.escape(title or "Resume")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title}</title>
  <style>
    @page {{
      size: A4;
      margin: 14mm 14mm 16mm;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      color: #1f2933;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      font-size: 13px;
      line-height: 1.58;
      margin: 0 auto;
      max-width: 820px;
      padding: 28px 32px 40px;
      background: #ffffff;
    }}
    h1 {{
      color: #111827;
      font-size: 25px;
      line-height: 1.25;
      margin: 0 0 14px;
    }}
    h2 {{
      border-bottom: 1px solid #d9e2ec;
      color: #111827;
      font-size: 17px;
      line-height: 1.35;
      margin: 24px 0 10px;
      padding-bottom: 5px;
    }}
    h3 {{
      color: #1f2933;
      font-size: 14px;
      line-height: 1.4;
      margin: 16px 0 6px;
    }}
    p {{
      margin: 4px 0 8px;
    }}
    ul {{
      margin: 4px 0 10px 18px;
      padding: 0;
    }}
    li {{
      margin: 2px 0;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def _markdown_to_html_body(markdown_text):
    html_lines = []
    in_list = False
    title = ""

    def close_list():
        nonlocal in_list
        if in_list:
            html_lines.append("</ul>")
            in_list = False

    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if not line:
            close_list()
            continue

        if line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"  <li>{html.escape(line[2:].strip())}</li>")
            continue

        close_list()
        if line.startswith("#"):
            marker, _, heading = line.partition(" ")
            if marker and set(marker) == {"#"} and heading:
                level = min(len(marker), 6)
                heading_text = html.escape(heading.strip())
                if level == 1 and not title:
                    title = heading.strip()
                html_lines.append(f"<h{level}>{heading_text}</h{level}>")
                continue

        html_lines.append(f"<p>{html.escape(line)}</p>")

    close_list()
    return "\n".join(html_lines), title


def _write_pdf_from_html(html_path, pdf_path):
    chrome = _find_chrome()
    if chrome is None:
        raise ResumeKitError("Google Chrome is required for PDF export", {"hint": "Install Chrome or export HTML only"})

    pdf_path = Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="resume-kit-chrome-") as user_data_dir:
        command = _build_chrome_pdf_command(chrome, user_data_dir, html_path, pdf_path)
        result = _run_chrome_print(command, pdf_path)
        if result.returncode != 0:
            command[1] = "--headless"
            result = _run_chrome_print(command, pdf_path)

    if result.returncode != 0 or not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise ResumeKitError(
            "PDF export failed",
            {
                "returncode": result.returncode,
                "stderr": result.stderr.strip(),
                "stdout": result.stdout.strip(),
            },
        )


def _build_chrome_pdf_command(chrome, user_data_dir, html_path, pdf_path):
    return [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-pdf-header-footer",
        f"--user-data-dir={user_data_dir}",
        f"--print-to-pdf={str(Path(pdf_path).resolve())}",
        Path(html_path).resolve().as_uri(),
    ]


def _run_chrome_print(command, pdf_path):
    pdf_path = Path(pdf_path)
    process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.monotonic() + 20
    last_size = -1
    stable_since = None

    while time.monotonic() < deadline:
        returncode = process.poll()
        if returncode is not None:
            stdout, stderr = process.communicate()
            return subprocess.CompletedProcess(command, returncode, stdout=stdout, stderr=stderr)

        if pdf_path.exists():
            size = pdf_path.stat().st_size
            if size > 0 and size == last_size:
                if stable_since is None:
                    stable_since = time.monotonic()
                elif time.monotonic() - stable_since >= 0.75:
                    return _finish_chrome_print(process, command, returncode=0)
            else:
                stable_since = None
                last_size = size

        time.sleep(0.2)

    return _finish_chrome_print(process, command, returncode=124, stderr_fallback="Chrome PDF export timed out")


def _finish_chrome_print(process, command, returncode, stderr_fallback=""):
    if process.poll() is None:
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
    else:
        stdout, stderr = process.communicate()
    return subprocess.CompletedProcess(command, returncode, stdout=stdout or "", stderr=stderr or stderr_fallback)


def _find_chrome():
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None
