#!/usr/bin/env python3
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from resume_kit.corpus import load_corpus
from resume_kit.errors import ResumeKitError
from resume_kit.jd import analyze_jd
from resume_kit.jsonio import emit_json, error_envelope, success_envelope
from resume_kit.llm_guardrails import build_llm_prompt
from resume_kit.matcher import match_jd
from resume_kit.package import create_package
from resume_kit.paths import PROJECT_ROOT, source_status
from resume_kit.profiles import get_profile, list_profiles
from resume_kit.renderers import render_gap, render_resume


def cmd_doctor(args):
    sources = source_status()
    data = {
        "project_root": str(PROJECT_ROOT),
        "source_root": "/Users/zego/my-code-wiki",
        "sources": sources,
    }
    warnings = [
        f"missing source: {item['path']}"
        for item in sources
        if not item["exists"]
    ]
    if args.json:
        emit_json(success_envelope(data, warnings=warnings))
    else:
        for item in sources:
            mark = "ok" if item["exists"] else "missing"
            print(f"{mark}: {item['key']} {item['path']}")
    return 0


def cmd_sources_list(args):
    data = {"sources": source_status()}
    if args.json:
        emit_json(success_envelope(data))
    else:
        for item in data["sources"]:
            mark = "ok" if item["exists"] else "missing"
            print(f"{mark}: {item['key']} {item['path']}")
    return 0


def cmd_profile_show(args):
    profile = get_profile(args.name)
    data = asdict(profile)
    if args.json:
        emit_json(success_envelope(data))
    else:
        print(profile.display_name)
        print(f"base resume: {profile.base_resume_key}")
        print("preferred projects:")
        for project in profile.preferred_projects:
            print(f"- {project}")
    return 0


def cmd_jd_analyze(args):
    jd = analyze_jd(Path(args.path).read_text(encoding="utf-8"))
    data = asdict(jd)
    if args.json:
        emit_json(success_envelope(data))
    else:
        print(jd.title)
        print(f"profile: {jd.inferred_profile}")
        print("keywords: " + ", ".join(jd.keywords))
        if jd.risk_flags:
            print("risk flags: " + ", ".join(jd.risk_flags))
    return 0


def _build_match(jd_path, profile_name):
    jd = analyze_jd(Path(jd_path).read_text(encoding="utf-8"))
    return match_jd(jd, get_profile(profile_name), load_corpus())


def cmd_match(args):
    result = _build_match(args.jd_path, args.profile)
    if args.json:
        emit_json(success_envelope(asdict(result)))
    else:
        print(f"profile: {result.profile}")
        print(f"direct matches: {len(result.direct_matches)}")
        print(f"gaps: {len(result.gaps)}")
    return 0


def _write_output(path, content, force=False):
    out_path = Path(path)
    if out_path.exists() and not force:
        raise ResumeKitError("Output file already exists", {"path": str(out_path)})
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


def cmd_resume_generate(args):
    result = _build_match(args.jd_path, args.profile)
    path = _write_output(args.out, render_resume(result), force=args.force)
    print(str(path))
    return 0


def cmd_gap_analyze(args):
    result = _build_match(args.jd_path, args.profile)
    path = _write_output(args.out, render_gap(result), force=args.force)
    print(str(path))
    return 0


def cmd_prompt_build(args):
    result = _build_match(args.jd_path, args.profile)
    path = _write_output(args.out, build_llm_prompt(result), force=args.force)
    print(str(path))
    return 0


def cmd_package(args):
    paths = create_package(args.jd_path, args.profile, args.out, force=args.force)
    data = {"paths": [str(path) for path in paths]}
    if args.json:
        emit_json(success_envelope(data))
    else:
        for path in paths:
            print(path)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="resume-kit")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="verify local sources and install state")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    sources = sub.add_parser("sources", help="inspect source files")
    sources_sub = sources.add_subparsers(dest="sources_command", required=True)
    sources_list = sources_sub.add_parser("list", help="list configured source files")
    sources_list.add_argument("--json", action="store_true")
    sources_list.set_defaults(func=cmd_sources_list)

    profile = sub.add_parser("profile", help="inspect resume profiles")
    profile_sub = profile.add_subparsers(dest="profile_command", required=True)
    profile_show = profile_sub.add_parser("show", help="show a profile")
    profile_show.add_argument("name", choices=[item.name for item in list_profiles()])
    profile_show.add_argument("--json", action="store_true")
    profile_show.set_defaults(func=cmd_profile_show)

    jd = sub.add_parser("jd", help="analyze job descriptions")
    jd_sub = jd.add_subparsers(dest="jd_command", required=True)
    jd_analyze = jd_sub.add_parser("analyze", help="analyze a JD markdown file")
    jd_analyze.add_argument("path")
    jd_analyze.add_argument("--json", action="store_true")
    jd_analyze.set_defaults(func=cmd_jd_analyze)

    match = sub.add_parser("match", help="match a JD against resume evidence")
    match.add_argument("jd_path")
    match.add_argument("--profile", required=True, choices=[item.name for item in list_profiles()])
    match.add_argument("--json", action="store_true")
    match.set_defaults(func=cmd_match)

    resume = sub.add_parser("resume", help="generate resume outputs")
    resume_sub = resume.add_subparsers(dest="resume_command", required=True)
    resume_generate = resume_sub.add_parser("generate", help="generate resume markdown")
    resume_generate.add_argument("jd_path")
    resume_generate.add_argument("--profile", required=True, choices=[item.name for item in list_profiles()])
    resume_generate.add_argument("--out", required=True)
    resume_generate.add_argument("--force", action="store_true")
    resume_generate.set_defaults(func=cmd_resume_generate)

    gap = sub.add_parser("gap", help="generate gap reports")
    gap_sub = gap.add_subparsers(dest="gap_command", required=True)
    gap_analyze = gap_sub.add_parser("analyze", help="generate gap markdown")
    gap_analyze.add_argument("jd_path")
    gap_analyze.add_argument("--profile", required=True, choices=[item.name for item in list_profiles()])
    gap_analyze.add_argument("--out", required=True)
    gap_analyze.add_argument("--force", action="store_true")
    gap_analyze.set_defaults(func=cmd_gap_analyze)

    prompt = sub.add_parser("prompt", help="build constrained LLM prompts")
    prompt_sub = prompt.add_subparsers(dest="prompt_command", required=True)
    prompt_build = prompt_sub.add_parser("build", help="build prompt markdown")
    prompt_build.add_argument("jd_path")
    prompt_build.add_argument("--profile", required=True, choices=[item.name for item in list_profiles()])
    prompt_build.add_argument("--out", required=True)
    prompt_build.add_argument("--force", action="store_true")
    prompt_build.set_defaults(func=cmd_prompt_build)

    package_parser = sub.add_parser("package", help="generate resume, gap, prompt, match, and evidence outputs")
    package_parser.add_argument("jd_path")
    package_parser.add_argument("--profile", required=True, choices=[item.name for item in list_profiles()])
    package_parser.add_argument("--out", required=True)
    package_parser.add_argument("--force", action="store_true")
    package_parser.add_argument("--json", action="store_true")
    package_parser.set_defaults(func=cmd_package)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ResumeKitError as exc:
        if getattr(args, "json", False):
            emit_json(error_envelope(exc.code, exc.message, exc.detail), stream=sys.stderr)
        else:
            print(f"error: {exc.message}", file=sys.stderr)
            if exc.detail:
                print(json.dumps(exc.detail, ensure_ascii=False), file=sys.stderr)
        return 1
    except FileExistsError as exc:
        if getattr(args, "json", False):
            emit_json(error_envelope("output_exists", "Output file already exists", {"path": str(exc)}), stream=sys.stderr)
        else:
            print(f"error: output already exists: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
