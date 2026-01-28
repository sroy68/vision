from core.memory import Memory

def main():
    mem = Memory("CHANGE_ME")
    print("=== Owner Override Console ===")
    while True:
        cmd = input("OWNER> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        elif cmd.lower() == "show memory":
            print(mem.data)
        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
