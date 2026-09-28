#!/bin/bash
# linux_password_reset.sh
# Resets a Linux user's password. Must be run as root.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'   # No Color

echo "=========================================="
echo "   LINUX PASSWORD RESET TOOL"
echo "=========================================="
echo

# Step 1: Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}ERROR: This tool must be run as root.${NC}"
    echo
    echo "On a real Linux system, use one of these:"
    echo "  1. sudo ./linux_password_reset.sh"
    echo "  2. Or boot into Recovery Mode and run as root"
    echo
    echo "In Termux on Android, this won't work (no root)."
    exit 1
fi

echo -e "${GREEN}Root access confirmed.${NC}"
echo

# Step 2: Show all users on the system
echo "=== Users on this system ==="
echo

# Get users with UID >= 1000 (normal users), plus root
USERS=$(awk -F: '$3 >= 1000 || $3 == 0 {print $1}' /etc/passwd | sort)

i=1
declare -a user_list
for user in $USERS; do
    echo "  $i. $user"
    user_list[$i]=$user
    i=$((i+1))
done
echo

# Step 3: Ask which user to reset
read -p "Choose user number: " choice

# Validate choice
if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -ge "$i" ]; then
    echo -e "${RED}Invalid choice.${NC}"
    exit 1
fi

TARGET_USER="${user_list[$choice]}"
echo
echo -e "${YELLOW}Resetting password for: $TARGET_USER${NC}"
echo

# Step 4: Confirm
read -p "Are you sure? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

# Step 5: Reset the password
echo
echo "Enter the new password when prompted."
echo "Note: the password won't show as you type."
echo

if passwd "$TARGET_USER"; then
    echo
    echo -e "${GREEN}✅ Password reset successfully for $TARGET_USER${NC}"

    # Step 6: Log the action
    LOG_FILE="/var/log/password_resets.log"
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$DATE] Password reset for: $TARGET_USER (by root)" >> "$LOG_FILE" 2>/dev/null
    echo "Logged to: $LOG_FILE"
else
    echo
    echo -e "${RED}❌ Password reset failed.${NC}"
    exit 1
fi

echo
echo "Done."
