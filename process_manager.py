class Process:
    def __init__(self, pid, user, command, cpu, memory, status="running"):
        self.pid = pid
        self.user = user
        self.command = command
        self.cpu = cpu
        self.memory = memory
        self.status = status


class ProcessManager:
    def __init__(self):
        self.total_memory = 4096

        self.processes = [
            Process(1, "system", "init", 0.5, 64),
            Process(2, "user", "terminal", 1.2, 120),
            Process(3, "user", "python", 5.8, 256),
            Process(4, "user", "file_system", 2.1, 80),
        ]

    def ps(self):
        print("PID   USER      CPU%   MEM(MB)   STATUS    COMMAND")

        for p in self.processes:
            print(
                f"{p.pid:<5} "
                f"{p.user:<9} "
                f"{p.cpu:<6} "
                f"{p.memory:<9} "
                f"{p.status:<9} "
                f"{p.command}"
            )

    def top(self):
        total_cpu = sum(p.cpu for p in self.processes)
        used_memory = sum(p.memory for p in self.processes)

        print(f"Tasks: {len(self.processes)} total")
        print(f"CPU usage: {total_cpu:.1f}%")
        print(f"Memory: {used_memory} / {self.total_memory} MB")
        print()
        print("PID   USER      CPU%   MEM(MB)   STATUS    COMMAND")

        sorted_processes = sorted(
            self.processes,
            key=lambda process: process.cpu,
            reverse=True
        )

        for p in sorted_processes:
            print(
                f"{p.pid:<5} "
                f"{p.user:<9} "
                f"{p.cpu:<6} "
                f"{p.memory:<9} "
                f"{p.status:<9} "
                f"{p.command}"
            )

    def free(self):
        used_memory = sum(p.memory for p in self.processes)
        free_memory = self.total_memory - used_memory

        print(f"Total Memory: {self.total_memory} MB")
        print(f"Used Memory : {used_memory} MB")
        print(f"Free Memory : {free_memory} MB")

    def kill(self, pid):
        for p in self.processes:
            if p.pid == pid:
                if p.pid == 1:
                    print("kill: cannot kill init process")
                    return

                self.processes.remove(p)
                print(f"process {pid} killed")
                return

        print(f"kill: {pid}: no such process")