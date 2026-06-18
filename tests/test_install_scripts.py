from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallScriptTests(unittest.TestCase):
    def test_unix_installer_downloads_release_binary_and_verifies_checksum(self) -> None:
        script = (ROOT / "docs" / "install.sh").read_text(encoding="utf-8")

        self.assertIn("https://github.com/${REPO}/releases", script)
        self.assertIn("/latest/download", script)
        self.assertIn("apollokairn-linux-x64.tar.gz", script)
        self.assertIn("apollokairn-linux-arm64.tar.gz", script)
        self.assertIn("apollokairn-macos-x64.tar.gz", script)
        self.assertIn("apollokairn-macos-arm64.tar.gz", script)
        self.assertIn("checksums.txt", script)
        self.assertIn("sha256sum", script)
        self.assertIn("shasum -a 256", script)
        self.assertIn("APOLLOKAIRN_INSTALL_DIR", script)
        self.assertIn("CAIRN_INSTALL_DIR", script)
        self.assertIn("apollokairn", script)
        self.assertIn("ak", script)
        self.assertIn("$HOME/.local/bin", script)
        self.assertNotIn("python -m pip", script)
        self.assertNotIn("pip install", script)

    def test_readmes_link_to_quick_install_guides(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_pt = (ROOT / "README.pt-BR.md").read_text(encoding="utf-8")

        self.assertIn("docs/guides/quick-install.md", readme)
        self.assertIn("docs/guides/quick-install.pt-BR.md", readme_pt)
        self.assertIn("<h1>ApolloKairn</h1>", readme)
        self.assertIn("<h1>ApolloKairn</h1>", readme_pt)
        self.assertIn("ApolloKairn was previously named Cairn", readme)
        self.assertIn("ApolloKairn se chamava Cairn", readme_pt)
        self.assertIn("curl -fsSL https://sinkz.github.io/apollokairn/install.sh | sh", readme)
        self.assertIn("irm https://sinkz.github.io/apollokairn/install.ps1 | iex", readme)
        self.assertIn("curl -fsSL https://sinkz.github.io/apollokairn/install.sh | sh", readme_pt)
        self.assertIn("irm https://sinkz.github.io/apollokairn/install.ps1 | iex", readme_pt)
        self.assertIn("apollokairn --version", readme)
        self.assertIn("apollokairn --version", readme_pt)

    def test_quick_install_guides_cover_path_troubleshooting_and_vault_creation(self) -> None:
        guide = (ROOT / "docs" / "guides" / "quick-install.md").read_text(encoding="utf-8")
        guide_pt = (ROOT / "docs" / "guides" / "quick-install.pt-BR.md").read_text(encoding="utf-8")

        for text in (guide, guide_pt):
            self.assertIn("install.sh", text)
            self.assertIn("install.ps1", text)
            self.assertIn("apollokairn --version", text)
            self.assertIn("apollokairn init", text)
            self.assertIn("APOLLOKAIRN_INSTALL_DIR", text)
            self.assertIn("CAIRN_INSTALL_DIR", text)
            self.assertIn("PATH", text)
            self.assertIn("checksums.txt", text)
            self.assertIn("GitHub Releases", text)

    def test_landing_links_to_installers_and_guides(self) -> None:
        page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

        self.assertIn("id=\"install\"", page)
        self.assertIn("id=\"benchmark-preview-cards\"", page)
        self.assertIn("benchmarks.html", page)
        self.assertNotIn("id=\"benchmark-suites\"", page)
        self.assertNotIn("id=\"benchmark-history\"", page)
        self.assertIn("ApolloKairn", page)
        self.assertIn("apollokairn --version", page)
        self.assertIn("https://github.com/sinkz/apollokairn", page)
        self.assertIn("curl -fsSL https://sinkz.github.io/apollokairn/install.sh | sh", page)
        self.assertIn("irm https://sinkz.github.io/apollokairn/install.ps1 | iex", page)
        self.assertIn("guides/quick-install.md", page)
        self.assertIn("guides/quick-install.pt-BR.md", page)

    def test_public_site_uses_apollokairn_links_and_storage_key(self) -> None:
        files = [
            ROOT / "docs" / "index.html",
            ROOT / "docs" / "learn.html",
            ROOT / "docs" / "benchmarks.html",
            ROOT / "docs" / "assets" / "site.js",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in files)

        self.assertIn("ApolloKairn", combined)
        self.assertIn("https://github.com/sinkz/apollokairn", combined)
        self.assertIn("apollokairn-lang", combined)
        self.assertNotIn("sinkz.github.io/cairn", combined)
        self.assertNotIn("github.com/sinkz/cairn", combined)

    def test_benchmark_page_contains_full_dashboard_mounts(self) -> None:
        page = (ROOT / "docs" / "benchmarks.html").read_text(encoding="utf-8")

        self.assertIn("id=\"benchmark-suites\"", page)
        self.assertIn("id=\"benchmark-history\"", page)
        self.assertIn("id=\"benchmark-preview-cards\"", page)
        self.assertIn("data-benchmark-page", page)
        self.assertIn("Recall@3", page)
        self.assertIn("nDCG@3", page)
        self.assertIn("context_reduction", page)

    def test_benchmark_history_uses_snapshot_for_short_history(self) -> None:
        script = (ROOT / "docs" / "assets" / "site.js").read_text(encoding="utf-8")

        self.assertIn("function renderHistorySnapshot", script)
        self.assertIn("history.length < 3", script)
        self.assertIn("history-snapshot", script)

    def test_benchmark_dashboard_renders_metric_deltas(self) -> None:
        script = (ROOT / "docs" / "assets" / "site.js").read_text(encoding="utf-8")
        styles = (ROOT / "docs" / "assets" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("function renderMetricDelta", script)
        self.assertIn("metric.delta", script)
        self.assertIn("metric-delta", script)
        self.assertIn("data-trend", script)
        self.assertIn(".metric-delta", styles)

    def test_release_workflow_builds_standalone_assets(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

        self.assertIn("tags:", workflow)
        self.assertIn("'v*'", workflow)
        self.assertIn("pyinstaller", workflow)
        self.assertIn("python:3.12-slim-bullseye", workflow)
        self.assertIn("Build Linux x64 standalone binary in Debian 11 container", workflow)
        self.assertIn("apt-get install -y --no-install-recommends binutils", workflow)
        self.assertIn("chown -R", workflow)
        self.assertIn("stat -c '%u:%g' /work", workflow)
        self.assertIn("ubuntu-24.04", workflow)
        self.assertIn("ubuntu-24.04-arm", workflow)
        self.assertIn("windows-latest", workflow)
        self.assertIn("macos-15-intel", workflow)
        self.assertIn("macos-15", workflow)
        self.assertIn("apollokairn-linux-x64.tar.gz", workflow)
        self.assertIn("apollokairn-linux-arm64.tar.gz", workflow)
        self.assertIn("apollokairn-windows-x64.zip", workflow)
        self.assertIn("apollokairn-macos-x64.tar.gz", workflow)
        self.assertIn("apollokairn-macos-arm64.tar.gz", workflow)
        self.assertIn("checksums.txt", workflow)
        self.assertIn("softprops/action-gh-release", workflow)

    def test_linux_x64_release_packaging_does_not_chmod_container_output(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

        self.assertIn("tar --mode='u+x,go+rx'", workflow)
        self.assertNotIn(
            "chmod +x dist/apollokairn\n          tar -czf release-assets/apollokairn-linux-x64.tar.gz",
            workflow,
        )

    def test_ci_runs_writeback_benchmark(self) -> None:
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        release = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

        command = "python bench/run_writeback_eval.py --quiet --compare-golden bench/writeback/golden.json"
        self.assertIn(command, ci)
        self.assertIn(command, release)

    def test_windows_installer_downloads_release_binary_and_verifies_checksum(self) -> None:
        script = (ROOT / "docs" / "install.ps1").read_text(encoding="utf-8")

        self.assertIn("https://github.com/$Repo/releases", script)
        self.assertIn("releases/latest/download", script)
        self.assertIn("apollokairn-windows-x64.zip", script)
        self.assertIn("checksums.txt", script)
        self.assertIn("Get-FileHash", script)
        self.assertIn("Expand-Archive", script)
        self.assertIn("APOLLOKAIRN_INSTALL_DIR", script)
        self.assertIn("CAIRN_INSTALL_DIR", script)
        self.assertIn("apollokairn.exe", script)
        self.assertIn("ak.exe", script)
        self.assertIn("LOCALAPPDATA", script)
        self.assertNotIn("python -m pip", script)
        self.assertNotIn("pip install", script)


if __name__ == "__main__":
    unittest.main()
