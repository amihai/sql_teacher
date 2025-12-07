#!/usr/bin/env bash
set -euo pipefail

# Nume user folosit de Ansible
USERNAME="ansible"

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 'SSH_PUBLIC_KEY'" >&2
  echo "Exemplu:"
  echo "  $0 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... user@host'"
  exit 1
fi

SSH_KEY="$1"

# 1. Cream userul ansible (daca nu exista deja)
if id "$USERNAME" &>/dev/null; then
  echo "Userul $USERNAME exista deja, sar peste creare."
else
  echo "Creez userul $USERNAME..."
  adduser --disabled-password --gecos "" "$USERNAME"
fi

# 2. Adaugam userul in grupul sudo
echo "Adaug $USERNAME in grupul sudo..."
usermod -aG sudo "$USERNAME"

# 3. Configuram sudo fara parola pentru userul ansible
SUDOERS_FILE="/etc/sudoers.d/${USERNAME}-nopasswd"
echo "Configurez sudo fara parola in $SUDOERS_FILE..."
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > "$SUDOERS_FILE"
chmod 440 "$SUDOERS_FILE"

# Validam fisierul de sudoers ca sa nu stricăm sudo
if ! visudo -cf "$SUDOERS_FILE" >/dev/null; then
  echo "Eroare: fisierul $SUDOERS_FILE nu este valid. Il sterg."
  rm -f "$SUDOERS_FILE"
  exit 1
fi

# 4. Setam cheia SSH in ~/.ssh/authorized_keys pentru userul ansible
USER_HOME=$(eval echo "~$USERNAME")
SSH_DIR="$USER_HOME/.ssh"
AUTH_KEYS="$SSH_DIR/authorized_keys"

echo "Setez cheia SSH pentru $USERNAME in $AUTH_KEYS..."

mkdir -p "$SSH_DIR"
touch "$AUTH_KEYS"

# Nu dublam cheia daca exista deja
if grep -qxF "$SSH_KEY" "$AUTH_KEYS"; then
  echo "Cheia SSH exista deja in authorized_keys, nu o mai adaug."
else
  echo "$SSH_KEY" >> "$AUTH_KEYS"
fi

# Permisiuni corecte
chmod 700 "$SSH_DIR"
chmod 600 "$AUTH_KEYS"
chown -R "$USERNAME:$USERNAME" "$SSH_DIR"

echo "Gata! Userul $USERNAME este creat, are sudo fara parola si cheia SSH este configurata."
echo "Poti testa cu:"
echo "  ssh $USERNAME@NUME_SAU_IP_MASINA"
