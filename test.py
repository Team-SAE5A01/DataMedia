import sh

# Run a simple shell command
print(sh.ls("-l"))

# Capture command output
output = sh.echo("Hello from sh!")
print(output)

# Run commands with sudo (prompting for a password)
# sh.sudo("apt-get", "update")
