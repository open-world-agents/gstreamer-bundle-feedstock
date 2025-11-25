#!/usr/bin/env python3
"""
Script to check for new GStreamer releases and update meta.yaml if needed.
"""

import os
import re
import sys

import requests
from packaging import version


def get_current_version():
    """Extract current GStreamer version from meta.yaml"""
    try:
        with open("recipe/meta.yaml", "r") as f:
            content = f.read()

        # Extract gst_version using regex
        match = re.search(r'{% set gst_version = "([^"]+)" %}', content)
        if match:
            return match.group(1)
        else:
            print("Could not find gst_version in meta.yaml")
            return None
    except Exception as e:
        print(f"Error reading meta.yaml: {e}")
        return None


def get_package_versions(package_name):
    """Get available versions for a specific conda-forge package"""
    try:
        url = f"https://api.anaconda.org/package/conda-forge/{package_name}"

        headers = {"User-Agent": "GStreamer-Bundle-Feedstock-Bot/1.0"}

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Get all versions - they are returned as strings in a list
        versions = data.get("versions", [])
        if not versions:
            return []

        # Filter for stable versions and sort
        stable_versions = []
        for version_str in versions:
            # Skip pre-releases, RCs, etc.
            if any(keyword in version_str.lower() for keyword in ["rc", "alpha", "beta", "pre", "dev"]):
                continue
            # Match version pattern like 1.24.0, 1.24.1, etc.
            if re.match(r"^\d+\.\d+\.\d+$", version_str):
                stable_versions.append(version_str)

        # Sort by version
        stable_versions.sort(key=lambda x: version.parse(x), reverse=True)
        return stable_versions

    except Exception as e:
        print(f"Error fetching versions for {package_name}: {e}")
        return []


def get_latest_gstreamer_version():
    """Get the latest GStreamer version that's available for ALL packages"""
    # List of all GStreamer packages we need to check
    gstreamer_packages = [
        "gstreamer",
        "gst-plugins-base",
        "gst-plugins-good",
        "gst-plugins-bad",
        "gst-plugins-ugly",
        "gst-libav",
        "gst-python",
    ]

    print("Checking versions for all GStreamer packages...")

    # Get versions for each package
    package_versions = {}
    for package in gstreamer_packages:
        print(f"  Checking {package}...")
        versions = get_package_versions(package)
        if not versions:
            print(f"    ❌ No versions found for {package}")
            return None, None, None
        package_versions[package] = versions
        print(f"    ✅ Latest: {versions[0]} (found {len(versions)} stable versions)")

    # Find the latest version that's available for ALL packages
    print("\nFinding common latest version...")

    # Start with the versions from the main gstreamer package
    common_versions = set(package_versions["gstreamer"])

    # Intersect with versions from all other packages
    for package, versions in package_versions.items():
        if package != "gstreamer":
            common_versions = common_versions.intersection(set(versions))
            print(f"  After checking {package}: {len(common_versions)} common versions")

    if not common_versions:
        print("❌ No common version found across all packages")
        return None, None, None

    # Get the latest common version
    common_versions_list = list(common_versions)
    common_versions_list.sort(key=lambda x: version.parse(x), reverse=True)

    latest_common_version = common_versions_list[0]
    release_url = f"https://anaconda.org/conda-forge/gstreamer/{latest_common_version}"

    print(f"✅ Latest common version: {latest_common_version}")
    print(f"   Available across {len(gstreamer_packages)} packages")

    return latest_common_version, "", release_url


def update_meta_yaml(new_version):
    """Update the meta.yaml file with the new version"""
    try:
        with open("recipe/meta.yaml", "r") as f:
            content = f.read()

        # Update both version and gst_version
        content = re.sub(r'{% set version = "[^"]+" %}', f'{{% set version = "{new_version}" %}}', content)
        content = re.sub(r'{% set gst_version = "[^"]+" %}', f'{{% set gst_version = "{new_version}" %}}', content)

        with open("recipe/meta.yaml", "w") as f:
            f.write(content)

        print(f"Updated meta.yaml with version {new_version}")
        return True

    except Exception as e:
        print(f"Error updating meta.yaml: {e}")
        return False


def get_package_status_summary(target_version):
    """Get a summary of package versions for the target version"""
    gstreamer_packages = [
        "gstreamer",
        "gst-plugins-base",
        "gst-plugins-good",
        "gst-plugins-bad",
        "gst-plugins-ugly",
        "gst-libav",
        "gst-python",
    ]

    status_lines = []
    for package in gstreamer_packages:
        versions = get_package_versions(package)
        if target_version in versions:
            status_lines.append(f"- ✅ **{package}**: `{target_version}`")
        else:
            latest = versions[0] if versions else "unknown"
            status_lines.append(f"- ❌ **{package}**: `{target_version}` (latest: `{latest}`)")

    return "\n".join(status_lines)


def set_github_output(name, value):
    """Set GitHub Actions output variable"""
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"Would set output: {name}={value}")


def main():
    print("Checking for new GStreamer versions...")

    # Get current version
    current_version = get_current_version()
    if not current_version:
        print("Failed to get current version")
        sys.exit(1)

    print(f"Current version: {current_version}")

    # Get latest version
    latest_version, release_date, release_url = get_latest_gstreamer_version()
    if not latest_version:
        print("Failed to get latest version")
        sys.exit(1)

    print(f"Latest version: {latest_version}")

    # Compare versions
    try:
        current_ver = version.parse(current_version)
        latest_ver = version.parse(latest_version)

        if latest_ver > current_ver:
            print(f"New version available: {latest_version}")

            # Update meta.yaml
            if update_meta_yaml(latest_version):
                # Set GitHub Actions outputs
                set_github_output("new-version-available", "true")
                set_github_output("current-version", current_version)
                set_github_output("new-version", latest_version)
                set_github_output("release-date", release_date)
                set_github_output("release-url", release_url)

                # Also output package status for PR description
                package_status = get_package_status_summary(latest_version)
                set_github_output("package-status", package_status)

                print("✅ Version update completed successfully")
            else:
                print("❌ Failed to update meta.yaml")
                sys.exit(1)
        else:
            print("✅ Already up to date")
            set_github_output("new-version-available", "false")

    except Exception as e:
        print(f"Error comparing versions: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
