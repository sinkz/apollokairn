#!/usr/bin/env sh
set -eu

REPO="${APOLLOKAIRN_REPO:-${CAIRN_REPO:-sinkz/apollokairn}}"
VERSION="${APOLLOKAIRN_VERSION:-${CAIRN_VERSION:-latest}}"
INSTALL_DIR="${APOLLOKAIRN_INSTALL_DIR:-${CAIRN_INSTALL_DIR:-$HOME/.local/bin}}"
RELEASES_URL="https://github.com/${REPO}/releases"
BINARY_NAME="apollokairn"
LEGACY_BINARY_NAME="cairn"
SHORT_ALIAS_NAME="ak"

# Expected release assets:
# - apollokairn-linux-x64.tar.gz
# - apollokairn-linux-arm64.tar.gz
# - apollokairn-macos-x64.tar.gz
# - apollokairn-macos-arm64.tar.gz

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: $1 is required." >&2
    exit 1
  fi
}

detect_asset() {
  os="$(uname -s)"
  arch="$(uname -m)"

  case "$os" in
    Linux)
      platform="linux"
      ;;
    Darwin)
      platform="macos"
      ;;
    *)
      echo "ERROR: unsupported operating system: $os" >&2
      exit 1
      ;;
  esac

  case "$arch" in
    x86_64|amd64)
      cpu="x64"
      ;;
    arm64|aarch64)
      cpu="arm64"
      ;;
    *)
      echo "ERROR: unsupported architecture: $arch" >&2
      exit 1
      ;;
  esac

  printf "apollokairn-%s-%s.tar.gz" "$platform" "$cpu"
}

download_base() {
  if [ "$VERSION" = "latest" ]; then
    printf "%s/latest/download" "$RELEASES_URL"
    return
  fi

  case "$VERSION" in
    v*) tag="$VERSION" ;;
    *) tag="v$VERSION" ;;
  esac
  printf "%s/download/%s" "$RELEASES_URL" "$tag"
}

verify_checksum() {
  asset="$1"
  checksum_file="$2"

  if ! grep "  $asset\$" "$checksum_file" > "$checksum_file.one"; then
    echo "ERROR: checksum for $asset was not found in checksums.txt." >&2
    exit 1
  fi

  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c "$checksum_file.one"
    return
  fi

  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 -c "$checksum_file.one"
    return
  fi

  echo "ERROR: sha256sum or shasum is required." >&2
  exit 1
}

need curl
need tar

ASSET="$(detect_asset)"
BASE_URL="$(download_base)"
TMP_DIR="${TMPDIR:-/tmp}/apollokairn-install-$$"
ARCHIVE="$TMP_DIR/$ASSET"
CHECKSUMS="$TMP_DIR/checksums.txt"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

mkdir -p "$TMP_DIR"
mkdir -p "$INSTALL_DIR"

echo "Downloading $ASSET from $BASE_URL"
curl -fsSL "$BASE_URL/$ASSET" -o "$ARCHIVE"
curl -fsSL "$BASE_URL/checksums.txt" -o "$CHECKSUMS"

(
  cd "$TMP_DIR"
  verify_checksum "$ASSET" "$CHECKSUMS"
  tar -xzf "$ARCHIVE"
)

if [ ! -f "$TMP_DIR/$BINARY_NAME" ]; then
  echo "ERROR: release archive did not contain an $BINARY_NAME binary." >&2
  exit 1
fi

cp "$TMP_DIR/$BINARY_NAME" "$INSTALL_DIR/$BINARY_NAME"
chmod 755 "$INSTALL_DIR/$BINARY_NAME"
cp "$INSTALL_DIR/$BINARY_NAME" "$INSTALL_DIR/$SHORT_ALIAS_NAME"
cp "$INSTALL_DIR/$BINARY_NAME" "$INSTALL_DIR/$LEGACY_BINARY_NAME"
chmod 755 "$INSTALL_DIR/$SHORT_ALIAS_NAME" "$INSTALL_DIR/$LEGACY_BINARY_NAME"

case ":$PATH:" in
  *":$INSTALL_DIR:"*) ;;
  *)
    echo "NOTE: $INSTALL_DIR is not currently in PATH."
    echo "Add this to your shell profile:"
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
    ;;
esac

"$INSTALL_DIR/$BINARY_NAME" --version
echo "Installed ApolloKairn at $INSTALL_DIR/$BINARY_NAME"
echo "Aliases installed: $SHORT_ALIAS_NAME, $LEGACY_BINARY_NAME"
