"""Simple terminal CLI for the National Park Tracker final project.

Usage examples:
  python main.py add-park --name "Yellowstone" --state "WY"
  python main.py list-parks
  python main.py add-visit --park "Yellowstone" --trail "Upper Loop" --party 3
  python main.py list-visits --park "Yellowstone"
  python main.py export --path export.json
"""

import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from finalproject import db

console = Console()


def cmd_add_park(args):
    p = db.add_park(name=args.name, state=args.state)
    console.print(f"Added park: [bold]{p.name}[/]")


def cmd_list_parks(args):
    parks = db.list_parks()
    # filter by visited/unvisited if requested
    if getattr(args, 'visited', False) or getattr(args, 'unvisited', False):
        visited_ids = db.get_visited_park_ids()
        if getattr(args, 'visited', False):
            parks = [p for p in parks if p.id in visited_ids]
        else:
            parks = [p for p in parks if p.id not in visited_ids]

    show_notes = getattr(args, 'show_notes', False)
    if show_notes:
        table = Table("Name", "State", "Lat", "Lon", "Notes")
    else:
        table = Table("Name", "State", "Lat", "Lon")
    for p in parks:
        lat = f"{p.lat:.6f}" if p.lat is not None else ""
        lon = f"{p.lon:.6f}" if p.lon is not None else ""
        if show_notes:
            note = p.notes or ""
            # truncate notes to 60 chars for table
            if len(note) > 60:
                note = note[:57] + '...'
            table.add_row(p.name, p.state or "", lat, lon, note)
        else:
            table.add_row(p.name, p.state or "", lat, lon)
    console.print(table)


def cmd_add_visit(args):
    park = db.find_park_by_name(args.park)
    if not park:
        console.print(f"Park '{args.park}' not found; create it first.")
        return
    v = db.add_visit(park_id=park.id, trail=args.trail, start=args.start, end=args.end, party_size=args.party)
    console.print(f"Added visit: {v.id} to park {park.name}")


def cmd_list_visits(args):
    park = None
    if args.park:
        park = db.find_park_by_name(args.park)
        if not park:
            console.print(f"Park '{args.park}' not found.")
            return
    visits = db.list_visits(park_id=park.id if park else None)
    table = Table("ID", "Park", "Trail", "Start", "End", "Party", "Created")
    for v in visits:
        park_rec = db.find_park_by_id(v.park_id)
        park_name = park_rec.name if park_rec else "Unknown"
        table.add_row(v.id, park_name, v.trail or "", v.start or "", v.end or "", str(v.party_size), v.created_at)
    console.print(table)


def cmd_visit_park(args):
    park = db.find_park_by_name(args.park)
    if not park:
        console.print(f"Park '{args.park}' not found; create it first.")
        return
    v = db.add_visit(park_id=park.id, trail=None, start=args.date, end=None, party_size=args.party, notes=args.notes)
    console.print(f"Marked visit to {park.name} (visit id={v.id})")


def cmd_note_park(args):
    park = db.find_park_by_name(args.park)
    if not park:
        console.print(f"Park '{args.park}' not found; create it first.")
        return
    db.update_park(park.id, notes=args.note)
    console.print(f"Saved note for {park.name}")


def cmd_export(args):
    db.export_json(args.path)
    console.print(f"Exported data to {args.path}")


def cmd_import_parks(args):
    src = args.source
    try:
        with open(src, 'r', encoding='utf-8') as f:
            parks = __import__('json').load(f)
    except FileNotFoundError:
        console.print(f"Source file not found: {src}")
        return
    except Exception as e:
        console.print(f"Failed to read source: {e}")
        return

    added = 0
    skipped = 0
    for rec in parks:
        name = rec.get('name') or rec.get('NAME')
        state = rec.get('state') or rec.get('STATES')
        lat = None
        lon = None
        source_id = None
        # try common keys for latitude/longitude and source id
        for k in ('lat', 'latitude', 'LATITUDE'):
            if rec.get(k) is not None:
                try:
                    lat = float(rec.get(k))
                except Exception:
                    lat = None
                break
        for k in ('lon', 'lng', 'longitude', 'LONGITUDE'):
            if rec.get(k) is not None:
                try:
                    lon = float(rec.get(k))
                except Exception:
                    lon = None
                break
        for k in ('id', 'PARK_CODE', 'park_code'):
            if rec.get(k) is not None:
                source_id = rec.get(k)
                break
        if not name:
            continue
        existing = db.find_park_by_name(name)
        if existing:
            # if existing record lacks lat/lon/source_id but source has them, update
            need_update = False
            upd = {}
            if (existing.lat is None or existing.lat == '') and lat is not None:
                upd['lat'] = lat
                need_update = True
            if (existing.lon is None or existing.lon == '') and lon is not None:
                upd['lon'] = lon
                need_update = True
            if (existing.source_id is None or existing.source_id == '') and source_id is not None:
                upd['source_id'] = source_id
                need_update = True
            if need_update:
                db.update_park(existing.id, **upd)
                added += 1
            else:
                skipped += 1
            continue
        db.add_park(name=name, state=state, lat=lat, lon=lon, source_id=source_id)
        added += 1

    console.print(f"Imported parks: added={added}, skipped={skipped}")


def cmd_menu(args):
    """Simple interactive menu for common actions."""
    while True:
        console.print("\n[bold]National Park Tracker - Menu[/]")
        console.print("1) List parks")
        console.print("2) Add park")
        console.print("3) Import parks from data/parks.json")
        console.print("4) List visits")
        console.print("5) Add visit")
        console.print("6) Launch AI agent")
        console.print("0) Exit")
        try:
            choice = input('Select an option: ').strip()
        except (EOFError, KeyboardInterrupt):
            console.print('\nExiting menu.')
            return

        if choice == '0':
            console.print('Goodbye.')
            return
        if choice == '1':
            cmd_list_parks(argparse.Namespace())
        elif choice == '2':
            name = input('Park name: ').strip()
            state = input('State (optional): ').strip() or None
            if name:
                db.add_park(name=name, state=state)
                console.print(f'Added park: {name}')
        elif choice == '3':
            cmd_import_parks(argparse.Namespace(source='data/parks.json'))
        elif choice == '4':
            park_name = input('Park name to filter (leave blank for all): ').strip() or None
            cmd_list_visits(argparse.Namespace(park=park_name))
        elif choice == '5':
            park_name = input('Park name: ').strip()
            trail = input('Trail (optional): ').strip() or None
            party = input('Party size (default 1): ').strip()
            try:
                party_i = int(party) if party else 1
            except ValueError:
                party_i = 1
            if park_name:
                cmd_add_visit(argparse.Namespace(park=park_name, trail=trail, start=None, end=None, party=party_i))
        elif choice == '6':
            console.print('Launching local AI agent (type "exit" to quit)')
            cmd_agent(argparse.Namespace(prompt=None))
        else:
            console.print('Unknown option')


def cmd_agent(args):
    """Local keyword-based AI agent. Safe, offline, and maps prompts to allowed actions.

    Supported actions (keyword matching):
    - import parks: loads `data/parks.json` into finalproject store
    - list parks: shows parks
    - add park <name> [state]: creates a park
    - add visit to <park> [party N]
    """
    def call_llm(prompt: str) -> str:
        """Call OpenAI and request a JSON intent response.

        Returns a dict with keys: action, params, explanation if successful, or None on any failure
        (including missing API key or missing `openai` package).
        """
        import os, json, re
        key = os.environ.get('OPENAI_API_KEY')
        if not key:
            return None
        try:
            import openai
        except Exception:
            return None
        openai.api_key = key
        system = (
            "You are a safe assistant for a terminal-based National Park Tracker. "
            "When given a user prompt, output a single JSON object (no surrounding commentary) describing at most one allowed action. "
            "Allowed actions: \"list_parks\", \"import_parks\", \"add_park\", \"add_visit\", \"none\". "
            "The JSON must have keys: action (string), params (object), explanation (string). "
            "Params for add_park: {name: string, state: string (optional)}. "
            "Params for add_visit: {park: string, trail: string (optional), start: string (optional), end: string (optional), party: int (optional)}. "
            "If you cannot map the prompt to a single allowed action, return action \"none\" and provide a short explanation."
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                max_tokens=256,
                temperature=0.0,
            )
            content = resp.choices[0].message.content.strip()
        except Exception:
            return None

        # Extract first JSON object from the model output
        m = re.search(r"\{.*\}", content, re.DOTALL)
        if not m:
            return None
        try:
            j = json.loads(m.group(0))
            return j
        except Exception:
            return None


    def call_llm_text(prompt: str) -> str:
        """Call OpenAI for a plain-text response; returns text or empty string on failure."""
        import os
        key = os.environ.get('OPENAI_API_KEY')
        if not key:
            return ""
        try:
            import openai
        except Exception:
            return ""
        openai.api_key = key
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            return ""


    def handle_prompt(text: str):
        t = text.lower().strip()
        if t in ('exit', 'quit'):
            return False
        # If asked to use an LLM, attempt it first and fall back to rules
        if args and getattr(args, 'use_llm', False):
            intent = call_llm(text)
            if intent is None:
                # no API key or failure; fall back to rule-based parsing
                console.print('[yellow]LLM unavailable or failed; falling back to local rules.[/]')
            else:
                # Expected JSON: {action: str, params: dict, explanation: str}
                action = intent.get('action')
                params = intent.get('params', {}) or {}
                explanation = intent.get('explanation', '')
                console.print('[yellow]LLM suggestion:[/]')
                if explanation:
                    console.print(explanation)
                console.print(f"Suggested action: [bold]{action}[/] with params {params}")
                # Ask for confirmation before executing anything
                try:
                    confirm = input('Execute suggested action? (y/n): ').strip().lower()
                except (EOFError, KeyboardInterrupt):
                    confirm = 'n'
                if confirm in ('y', 'yes'):
                    if action == 'import_parks':
                        cmd_import_parks(argparse.Namespace(source='data/parks.json'))
                        return True
                    if action == 'list_parks':
                        cmd_list_parks(argparse.Namespace())
                        return True
                    if action == 'add_park':
                        name = params.get('name')
                        state = params.get('state')
                        if name:
                            db.add_park(name=name, state=state)
                            console.print(f'Agent: added park {name} ({state or ""})')
                        else:
                            console.print('Agent: add_park missing required param "name"')
                        return True
                    if action == 'add_visit':
                        park_name = params.get('park')
                        if not park_name:
                            console.print('Agent: add_visit missing required param "park"')
                            return True
                        trail = params.get('trail')
                        start = params.get('start')
                        end = params.get('end')
                        party = int(params.get('party', 1) or 1)
                        cmd_add_visit(argparse.Namespace(park=park_name, trail=trail, start=start, end=end, party=party))
                        return True
                    console.print('Agent: action not recognized or not allowed')
                    return True
        # find parks by state: "find parks in CA" or "parks in California"
        if ('find' in t or 'parks' in t) and ' in ' in t:
            # extract state token after ' in '
            try:
                state_q = t.split(' in ', 1)[1].strip()
                # list parks and filter by state substring
                parks = [p for p in db.list_parks() if p.state and state_q.upper() in p.state.upper()]
                table = Table("Name", "State", "Lat", "Lon")
                for p in parks:
                    lat = f"{p.lat:.6f}" if p.lat is not None else ""
                    lon = f"{p.lon:.6f}" if p.lon is not None else ""
                    table.add_row(p.name, p.state or "", lat, lon)
                console.print(table)
            except Exception:
                console.print('Agent: could not parse state query')
            return True

        # plan visit: "plan visit to Yellowstone on 2025-07-10 for 3"
        if 'plan' in t and 'visit' in t and ' to ' in t:
            try:
                rest = text.split(' to ', 1)[1]
                park_part = rest
                date_part = None
                party = 1
                if ' on ' in rest:
                    park_part, after = rest.split(' on ', 1)
                    park_part = park_part.strip()
                    if ' for ' in after:
                        date_str, after2 = after.split(' for ', 1)
                        date_part = date_str.strip()
                        try:
                            party = int(after2.strip().split()[0])
                        except Exception:
                            party = 1
                    else:
                        date_part = after.strip()
                park_name = park_part.strip()
                start_date = None
                if date_part:
                    try:
                        from dateutil import parser as dateparser
                        start_date = dateparser.parse(date_part).date().isoformat()
                    except Exception:
                        start_date = None
                if park_name:
                    cmd_add_visit(argparse.Namespace(park=park_name, trail=None, start=start_date, end=None, party=party))
                    console.print(f'Agent: planned visit to {park_name} on {start_date or "(no date)"} for {party} people')
                else:
                    console.print('Agent: could not parse park name for plan visit')
            except Exception:
                console.print('Agent: error parsing plan visit command')
            return True

        if 'import' in t and 'park' in t:
            console.print('Agent: importing parks from data/parks.json')
            cmd_import_parks(argparse.Namespace(source='data/parks.json'))
            return True
        if 'list' in t and 'park' in t:
            console.print('Agent: listing parks')
            cmd_list_parks(argparse.Namespace())
            return True
        if t.startswith('add park'):
            rest = text[len('add park'):].strip()
            if not rest:
                console.print('Agent: please provide a park name after "add park"')
                return True
            parts = [p.strip().strip(',') for p in rest.replace(',', ' ').split()]
            state = None
            name = rest
            if len(parts) >= 2 and len(parts[-1]) <= 3:
                state = parts[-1]
                name = ' '.join(parts[:-1])
            db.add_park(name=name, state=state)
            console.print(f'Agent: added park {name} ({state or ""})')
            return True
        if t.startswith('add visit') or ('add' in t and 'visit' in t):
            park = None
            party = 1
            if ' to ' in t:
                park = text.split(' to ', 1)[1].split()[0]
            import re
            m = re.search(r'party\s+(\d+)', t)
            if m:
                try:
                    party = int(m.group(1))
                except Exception:
                    party = 1
            if park:
                cmd_add_visit(argparse.Namespace(park=park, trail=None, start=None, end=None, party=party))
                console.print(f'Agent: added visit to {park} (party {party})')
            else:
                console.print('Agent: could not parse park name for visit. Try "add visit to <park> party N"')
            return True

        console.print('Agent: I did not understand that. Try: "import parks", "list parks", "add park <name>", or "add visit to <park> party N"')
        return True

    if args.prompt:
        handle_prompt(args.prompt)
        return

    while True:
        try:
            text = input('agent> ')
        except (EOFError, KeyboardInterrupt):
            console.print('\nAgent session closed')
            return
        cont = handle_prompt(text)
        if cont is False:
            console.print('Agent: exiting')
            return


def build_parser():
    parser = argparse.ArgumentParser(prog="tracker")
    sub = parser.add_subparsers(dest='cmd')

    p_add_park = sub.add_parser('add-park')
    p_add_park.add_argument('--name', required=True)
    p_add_park.add_argument('--state', required=False)
    p_add_park.set_defaults(func=cmd_add_park)

    p_list_parks = sub.add_parser('list-parks')
    group = p_list_parks.add_mutually_exclusive_group()
    group.add_argument('--visited', action='store_true', help='show only parks you have visited')
    group.add_argument('--unvisited', action='store_true', help='show only parks you have not visited')
    p_list_parks.add_argument('--show-notes', action='store_true', help='display personal notes column')
    p_list_parks.set_defaults(func=cmd_list_parks)

    p_add_visit = sub.add_parser('add-visit')
    p_add_visit.add_argument('--park', required=True, help='park name')
    p_add_visit.add_argument('--trail', required=False)
    p_add_visit.add_argument('--start', required=False)
    p_add_visit.add_argument('--end', required=False)
    p_add_visit.add_argument('--party', type=int, default=1)
    p_add_visit.set_defaults(func=cmd_add_visit)

    p_visit_park = sub.add_parser('visit-park')
    p_visit_park.add_argument('--park', required=True, help='park name to mark visited')
    p_visit_park.add_argument('--date', required=False, help='visit start date (ISO or parseable)')
    p_visit_park.add_argument('--party', type=int, default=1)
    p_visit_park.add_argument('--notes', required=False)
    p_visit_park.set_defaults(func=cmd_visit_park)

    p_note = sub.add_parser('note-park')
    p_note.add_argument('--park', required=True, help='park name to add/edit note')
    p_note.add_argument('--note', required=True, help='personal note text')
    p_note.set_defaults(func=cmd_note_park)

    p_list_visits = sub.add_parser('list-visits')
    p_list_visits.add_argument('--park', required=False, help='park name')
    p_list_visits.set_defaults(func=cmd_list_visits)

    p_export = sub.add_parser('export')
    p_export.add_argument('--path', required=True)
    p_export.set_defaults(func=cmd_export)

    p_import = sub.add_parser('import-parks')
    p_import.add_argument('--source', required=False, default='data/parks.json', help='path to parks JSON (default: data/parks.json)')
    p_import.set_defaults(func=cmd_import_parks)

    p_menu = sub.add_parser('menu')
    p_menu.set_defaults(func=cmd_menu)

    p_agent = sub.add_parser('agent')
    p_agent.add_argument('--prompt', required=False, help='one-shot prompt for the local AI agent')
    p_agent.add_argument('--use-llm', action='store_true', help='use an external LLM (requires OPENAI_API_KEY in environment)')
    p_agent.set_defaults(func=cmd_agent)

    return parser


def main(argv=None):
    db.init_db()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    args.func(args)


if __name__ == '__main__':
    main()
