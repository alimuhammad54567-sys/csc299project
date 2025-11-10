import json
import os
import random

DATA_FILE = "parks.json"

# Valid US state codes
STATE_CODES = {
    "al","ak","az","ar","ca","co","ct","de","fl","ga","hi","id","il","in","ia",
    "ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj",
    "nm","ny","nc","nd","oh","ok","or","pa","ri","sc","sd","tn","tx","ut","vt",
    "va","wa","wv","wi","wy"
}

# Mapping of state codes to ASCII map coordinates (row, column)
STATE_COORDS = {
    "wa": (2, 6), "or": (3, 5), "ca": (10, 5), "id": (5, 9), "nv": (10, 6),
    "ut": (10, 8), "az": (13, 6), "mt": (4, 15), "wy": (7, 15), "co": (10, 15),
    "nm": (14, 8), "nd": (3, 20), "sd": (5, 20), "ne": (6, 20), "ks": (10, 18),
    "ok": (12, 18), "tx": (16, 15), "mn": (2, 25), "ia": (5, 25), "mo": (10, 22),
    "ar": (13, 22), "la": (16, 22), "wi": (4, 30), "il": (6, 28), "ms": (14, 22),
    "mi": (2, 35), "in": (6, 32), "oh": (5, 35), "ky": (10, 32), "tn": (12, 32),
    "al": (14, 32), "ga": (13, 35), "fl": (17, 35), "sc": (15, 35), "nc": (12, 35),
    "va": (11, 35), "wv": (9, 34), "pa": (7, 34), "ny": (3, 38), "vt": (2, 38),
    "nh": (2, 39), "me": (1, 40), "ma": (2, 39), "ct": (3, 40), "ri": (3, 41),
    "nj": (5, 38), "de": (6, 38), "md": (6, 37)
}

# ASCII map of the US
USA_MAP = [
    "      ,__                                                   _,",
    "     \\~\\|  ~~---___              ,                          | \\",
    "      | Wash./ |   ~~~~~~~|~~~~~| ~~---,                VT_/,ME>",
    "     /~-_--__| |  Montana |N Dak\\ Minn/ ~\\~~/Mich.     /~| ||,' ",
    "    |Oregon /  \\         |------|   { WI / /~)     __-NY',|_\\,NH",
    "   /       |Ida.|~~~~~~~~|S Dak.\\    \\   | | '~\\  |_____,|~,-'Mass.",
    "   |~~--__ |    | Wyoming|____  |~~~~~|--| |__ /_-'Penn.{,~Conn (RI)",
    "   |   |  ~~~|~~|        |    ~~\\ Iowa/  `-' |`~ |~_____{/NJ",
    "   |   |     |  '---------, Nebr.\\----| IL|IN|OH,' ~/~\\,|`MD (DE)",
    "   ',  \\ Nev.|Utah| Colo. |~~~~~~~|    \\  | ,'~~\\WV/ VA |",
    "    |Cal\\    |    |       | Kansas| MO  \\_-~ KY /`~___--\\",
    "    ',   \\  ,-----|-------+-------'_____/__----~~/N Car./",
    "     '_   '\\|     |      |~~~|Okla.|    | Tenn._/-,~~-,/",
    "       \\    |Ariz.| New  |   |_    |Ark./~~|~~\\    \\,/S Car.",
    "        ~~~-'     | Mex. |     `~~~\\___|MS |AL | GA /",
    "            '-,_  | _____|          |  /   | ,-'---~\\",
    "                `~'~  \\    Texas    |LA`--,~~~~-~~,FL\\",
    "                       \\/~\\      /~~~`---`         |  \\",
    "                           \\    /                   \\  |",
    "                            \\  |                     '\\'",
    "                             `~'"
]

class ParkTracker:
    def __init__(self):
        self.parks = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.parks = json.load(f)
        else:
            self.parks = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.parks, f, indent=4)

    def add_park(self, name, state):
        state = state.lower()
        if state not in STATE_CODES:
            print(f"Invalid state code: {state}. Try again.")
            return
        self.parks.append({
            "name": name,
            "state": state,
            "visited": False,
            "notes": []
        })
        self.save_data()
        print(f"Added {name} in {state.upper()}")

    def list_parks(self):
        if not self.parks:
            print("No parks saved yet.")
            return
        for i, park in enumerate(self.parks, 1):
            status = "✅ Visited" if park["visited"] else "🟠 Not Visited"
            print(f"{i}. {park['name']} ({park['state'].upper()}) - {status}")

    def mark_visited(self, name):
        for park in self.parks:
            if park["name"].lower() == name.lower():
                park["visited"] = True
                self.save_data()
                print(f"{name} marked as visited!")
                return
        print(f"No park named {name} found.")

    def add_note(self, name, note):
        for park in self.parks:
            if park["name"].lower() == name.lower():
                park["notes"].append(note)
                self.save_data()
                print(f"Added note to {name}")
                return
        print(f"No park named {name} found.")

    def ai_suggest(self, keyword=None):
        if not self.parks:
            print("AI: Add some parks first!")
            return

        unvisited = [p for p in self.parks if not p["visited"]]
        if keyword:
            unvisited = [p for p in unvisited if keyword.lower() in p["name"].lower() or any(keyword.lower() in n.lower() for n in p["notes"])]

        if not unvisited:
            print("AI: No suggestions found for that keyword.")
            return

        choice = random.choice(unvisited)
        print(f"AI: You should check out {choice['name']} in {choice['state'].upper()} next!")

    def draw_map(self):
        # Make a mutable copy of ASCII map
        map_grid = [list(line) for line in USA_MAP]

        for park in self.parks:
            code = park["state"]
            if code in STATE_COORDS:
                r, c = STATE_COORDS[code]
                map_grid[r][c] = "X" if park["visited"] else "O"

        print("\n🗺️  US National Park Map\n")
        for line in map_grid:
            print("".join(line))
        print("\nLegend: X = Visited, O = Not Visited\n")

    def ai_chat(self):
        print("\n🤖 AI Agent Mode (type 'exit' to return)\n")
        while True:
            user_input = input("You: ").strip().lower()
            if user_input in ["exit", "quit", "back"]:
                print("Leaving AI mode...\n")
                break
            elif "suggest" in user_input or "recommend" in user_input:
                keyword = None
                if "hiking" in user_input:
                    keyword = "hiking"
                self.ai_suggest(keyword)
            elif "visited" in user_input:
                visited = [p["name"] for p in self.parks if p["visited"]]
                print("AI: You've visited:", ", ".join(visited) if visited else "no parks yet.")
            elif "map" in user_input:
                self.draw_map()
            elif "list" in user_input:
                self.list_parks()
            else:
                responses = [
                    "AI: I'm still learning about parks.",
                    "AI: Try asking me to 'suggest a park' or 'show the map'.",
                    "AI: You can type 'list' to see your parks.",
                ]
                print(random.choice(responses))


def main():
    tracker = ParkTracker()
    print("🌲 Welcome to the National Park Tracker 🌲")
    print("Commands: add/list/visit/note/ai/map/quit")

    while True:
        command = input("\nEnter command: ").strip().lower()
        if command == "add":
            name = input("Park name: ")
            state = input("State code (e.g., CA, AZ): ")
            tracker.add_park(name, state)
        elif command == "list":
            tracker.list_parks()
        elif command == "visit":
            name = input("Park name to mark visited: ")
            tracker.mark_visited(name)
        elif command == "note":
            name = input("Park name to add note: ")
            note = input("Your note: ")
            tracker.add_note(name, note)
        elif command == "ai":
            tracker.ai_chat()
        elif command == "map":
            tracker.draw_map()
        elif command == "quit":
            print("Goodbye! 🌎")
            break
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()
