#!/usr/bin/bash
#this will automate the process of transfaerring the script commands
#to the remote servers.
# Check if the user provided the filename as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Assign the first argument (filename) to a variable
filename="$1"

# Check if the file exists locally
if [ ! -f "$filename" ]; then
    echo "File '$filename' not found in the current directory."
    exit 1
fi

# Input server details
read -p "Enter the server's username: " username
read -p "Enter the server's IP address or hostname: " server_ip
read -p "Enter the remote directory path (e.g., /path/to/remote/directory/): " remote_dir

# Transfer the file to the server using scp
scp "$filename" "$username@$server_ip:$remote_dir"

# SSH into the server and execute the script
ssh "$username@$server_ip" "cd $remote_dir && chmod +x $filename && ./$filename"

# Optional: Provide a message upon completion
echo "Script '$filename' has been transferred and executed on the remote server."
