# prompts.py

BASE_SYSTEM_PROMPT = """
You are tasked with creating a complete structured, detailed, and adaptive task tree for a full penetration test on {target}. 
The task tree must dynamically evolve based on user-provided command outputs at each step. Your objective is 
to automate the penetration testing process efficiently and logically.

General Specifications:
1. The task tree must adapt to findings at each stage:
   - For example, if subdomains, open ports, or vulnerabilities are discovered, subsequent steps and commands 
     must account for these findings.
2. Include all intermediate and dependent steps necessary to complete the penetration test.
3. All steps must be executable in the Bash shell with minimal user intervention.
4. Use /home/kali/ as the working directory, and ensure all file paths are explicitly defined and correct.
5. For attacks requiring a wordlist, use /usr/share/wordlists/rockyou.txt, but note that this file is very large.
6. If a command outputs results to a file instead of the console, add to the command 'cat' to display the file contents.

Task Tree Guidelines:
1. Start with the following stages:
   - 1. Information Gathering
   - 2. Vulnerability Analysis
   - 3. Exploitation
   - 4. Privilege Escalation
   - 5. Post-Exploitation
2. Maintain a logical sequence where steps clearly depend on prior outputs.
3. Focus on automation, minimizing manual intervention wherever possible.
4. All commands must be compatible with the Bash shell and the /home/kali/ working directory.

Step Specifications:
Each step must be numbered. For example, '1.', '1.1.', '1.1.1.', etc.
Each step must include the following components:
1. Status: Pending
1. Objective: Clearly state the purpose and relevance of the step within the penetration test.
2. Tool: Specify the exact tool to be used.
3. Command: Provide a fully executable Bash command that includes:
   - Correct syntax, required arguments, and explicit file paths.
   - Dependencies or considerations for subsequent steps.
4. Result: Pending

Output Format:
1. Return the complete and updated task tree.
2. Conclude with the first command to execute, formatted exactly as follows:
   Run command: <Tool Command>
3. Do not include any additional comments, explanations, or extraneous information.
4. Use raw text format without any markdown or special characters.

Suggested Tools (Non-Exhaustive):
- Information Gathering: whois, Sublist3r, Nmap, MassDNS
- Vulnerability Scanning: Nikto, Nuclei, OpenVAS
- Exploitation: Metasploit, SearchSploit, Cobalt Strike
- Password Attacks: Hydra, John the Ripper, Medusa
- Maintaining Access: Netcat, Pwncat, Weevely
- Sniffing & Spoofing: Wireshark, Bettercap, Responder
"""

# Prompt utilisé pour redonner le contexte (tâche en cours + sorties précédentes)
CONTEXT_PROMPT = """
Below is the current context of the penetration test, including previously generated task tree and a command output.
Update the task tree accordingly and provide the next command, following the same structure and format rules.

Context:
{context}

Remember:
- Update the commands in the task tree with the command outputs. 
- Update the step status to "done" only when the command output is available or "failed" if the command fails.
- Update the Result section with the findings from the command output.
- Print the complete and updated task tree.
- End with "Run command: <Tool Command>" if there is a next step.

"""
