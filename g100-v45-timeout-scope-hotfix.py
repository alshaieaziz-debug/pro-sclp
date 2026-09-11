from pathlib import Path
root=Path('/opt/g100-hunter')
head=(root/'.git').exists()

def rep(path,old,new):
    p=root/path
    s=p.read_text()
    if old not in s:
        raise SystemExit(f'missing expected text in {path}: {old[:80]!r}')
    p.write_text(s.replace(old,new,1))

rep(Path('scripts/g100_provider_broker.py'),
'''    elif detected == "timeout":\n        set_cooldown(provider, "timeout", TIMEOUT_SECONDS)''',
'''    elif detected == "timeout":\n        set_model_cooldown(model,"timeout",TIMEOUT_SECONDS)''')
rep(Path('scripts/g100_provider_broker.py'),
'''        elif result.get("reason") in {"rate_limit","auth","timeout"}:\n            failed_providers.add(provider)''',
'''        elif result.get("reason") in {"rate_limit","auth"}:\n            failed_providers.add(provider)''')
rep(Path('scripts/g100_control_plane_v45.py'),
'''        if reason=="upstream" and model:\n            cmd=[sys.executable,str(BROKER),"cooldown-model",model,reason]''',
'''        if reason in {"upstream","timeout"} and model:\n            cmd=[sys.executable,str(BROKER),"cooldown-model",model,reason]''')
rep(Path('scripts/g100_control_plane_v45.py'),
'''            avoid_provider=provider if reason in {"rate_limit","auth","daily_quota","timeout"} else None''',
'''            avoid_provider=provider if reason in {"rate_limit","auth","daily_quota"} else None''')
rep(Path('scripts/g100_provider_broker.py'),
'''    if args.command == "cooldown-model":\n        set_model_cooldown(args.model,args.reason,UPSTREAM_MODEL_SECONDS); return''',
'''    if args.command == "cooldown-model":\n        seconds=TIMEOUT_SECONDS if args.reason=="timeout" else UPSTREAM_MODEL_SECONDS\n        set_model_cooldown(args.model,args.reason,seconds); return''')
print('HOTFIX_APPLIED')
