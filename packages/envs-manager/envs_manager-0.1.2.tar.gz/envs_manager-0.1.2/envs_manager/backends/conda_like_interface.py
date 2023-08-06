# SPDX-FileCopyrightText: 2022-present Spyder Development Team and envs-manager contributors
#
# SPDX-License-Identifier: MIT

import json
from pathlib import Path
import subprocess

import yaml
import requests

from envs_manager.api import EnvManagerInstance, run_command, get_package_info

MICROMAMBA_VARIANT = "micromamba"
CONDA_VARIANT = "conda"


class CondaLikeInterface(EnvManagerInstance):
    ID = "conda-like"

    def validate(self):
        if self.external_executable:
            command = [self.external_executable, "--version"]
            try:
                result = run_command(command, capture_output=True)
                version = result.stdout.split()
                if len(version) <= 1:
                    self.executable_variant = MICROMAMBA_VARIANT
                else:
                    self.executable_variant = version[0]
                return True
            except Exception as error:
                print(error.stderr)
        return False

    def create_environment(self, packages=[], channels=["conda-forge"], force=False):
        command = [self.external_executable, "create", "-p", self.environment_path]
        if packages:
            command += packages
        if channels:
            command += ["-c"] + channels
        if force:
            command += ["-y"]
        try:
            result = run_command(command, capture_output=True)
            print(result.stdout)
            return (True, result)
        except Exception as error:
            return (False, f"{error.returncode}: {error.stderr}")

    def delete_environment(self, force=False):
        command = [
            self.external_executable,
            "remove",
            "-p",
            self.environment_path,
            "--all",
        ]
        if force:
            command += ["-y"]
        try:
            result = run_command(command, capture_output=True)
            print(result.stdout)
            return (True, result)
        except Exception as error:
            return (False, f"{error.returncode}: {error.stderr}")

    def activate_environment(self):
        raise NotImplementedError()

    def deactivate_environment(self):
        raise NotImplementedError()

    def export_environment(self, export_file_path=None):
        command = [
            self.external_executable,
            "env",
            "export",
            "-p",
            self.environment_path,
            "--from-history",
        ]
        try:
            result = run_command(command, capture_output=True)
            if export_file_path:
                with open(export_file_path, "w") as exported_file:
                    exported_file.write(result.stdout)
                print(result.stdout)
            return (True, result)
        except subprocess.CalledProcessError as error:
            return (False, f"{error.returncode}: {error.stderr}")

    def import_environment(self, import_file_path, force=False):
        if self.executable_variant == MICROMAMBA_VARIANT:
            command = [
                self.external_executable,
                "create",
                "-p",
                self.environment_path,
                f"--file={import_file_path}",
            ]
            if force:
                command += ["-y"]
        else:
            command = [
                self.external_executable,
                "env",
                "create",
                "-p",
                self.environment_path,
                f"--file={import_file_path}",
            ]
            if force:
                command += ["--force"]
        try:
            result = run_command(command, capture_output=True)
            print(result.stdout)
            return (True, result)
        except subprocess.CalledProcessError as error:
            return (
                False,
                f"{error.returncode}: {error.stderr}\nNote: Importing environments only works for environment definitions created with the same operating system.",
            )

    def install_packages(
        self,
        packages,
        channels=["conda-forge"],
        force=False,
        capture_output=False,
    ):
        if self.executable_variant != MICROMAMBA_VARIANT:
            packages = [f"'{package}'" for package in packages]
        command = [
            self.external_executable,
            "install",
            "-p",
            self.environment_path,
        ] + packages
        if force:
            command += ["-y"]
        if channels:
            channels = ["-c"] + channels
            command += channels
        try:
            result = run_command(command, capture_output=capture_output)
            return (True, result)
        except subprocess.CalledProcessError as error:
            formatted_error = f"{error.returncode}: {error.stderr}"
            return (False, formatted_error)

    def uninstall_packages(self, packages, force=False, capture_output=False):
        command = [
            self.external_executable,
            "remove",
            "-p",
            self.environment_path,
        ] + packages
        if force:
            command += ["-y"]
        try:
            result = run_command(command, capture_output=capture_output)
            return (True, result)
        except subprocess.CalledProcessError as error:
            if "PackagesNotFoundError" in error.stderr:
                return (True, error)
            formatted_error = f"{error.returncode}: {error.stderr}"
            return (False, formatted_error)

    def update_packages(self, packages, force=False, capture_output=False):
        command = [
            self.external_executable,
            "update",
            "-p",
            self.environment_path,
        ] + packages
        if force:
            command += ["-y"]
        try:
            result = run_command(command, capture_output=capture_output)
            if capture_output:
                if "All requested packages already installed" in result.stdout:
                    return (False, result.stdout)
            else:
                return (True, result)
        except subprocess.CalledProcessError as error:
            formatted_error = f"{error.returncode}: {error.stderr}"
            return (False, formatted_error)

    def list_packages(self):
        command = [self.external_executable, "list", "-p", self.environment_path]
        result = run_command(command, capture_output=True)
        result_lines = result.stdout.split("\n")
        export_env_result, export_env_data = self.export_environment()
        if export_env_result:
            packages_requested = yaml.load(
                export_env_data.stdout, Loader=yaml.FullLoader
            )["dependencies"]
            packages_requested = [
                package.split("[")[0].split("=")[0] for package in packages_requested
            ]
        else:
            packages_requested = []

        if self.executable_variant == MICROMAMBA_VARIANT:
            skip_lines = 4
        else:
            skip_lines = 3
        formatted_packages = []
        formatted_list = dict(
            environment=self.environment_path, packages=formatted_packages
        )

        for package in result_lines[skip_lines:-1]:
            package_info = package.split()
            package_name = package_info[0]
            package_build = None if len(package_info) <= 2 else package_info[2]
            package_channel = None if len(package_info) <= 3 else package_info[3]
            package_full_info = get_package_info(package_name, channel=package_channel)
            package_description = (
                package_full_info["info"]["summary"] if package_full_info else None
            )
            package_requested = package_name in packages_requested
            formatted_package = dict(
                name=package_name,
                version=package_info[1],
                build=package_build,
                channel=package_channel,
                description=package_description,
                requested=package_requested,
            )
            formatted_packages.append(formatted_package)

        print(result.stdout)
        return (True, formatted_list)

    @classmethod
    def list_environments(cls, root_path, external_executable=None):
        if not external_executable:
            raise Exception(f"Missing path to external executable for {cls.ID} backend")
        envs_directory = Path(root_path) / cls.ID / "envs"
        environments = {}
        envs_directory.mkdir(parents=True, exist_ok=True)
        command = [external_executable, "env", "list", "--json"]
        try:
            result = run_command(command, capture_output=True)
            print(result.stdout)
            result_json = json.loads(result.stdout)
            for env_dir in result_json["envs"]:
                env_dir_path = Path(env_dir)
                if envs_directory in env_dir_path.parents:
                    environments[env_dir_path.name] = str(env_dir_path)
            return (environments, result)
        except subprocess.CalledProcessError as error:
            formatted_error = f"{error.returncode}: {error.stderr}"
            return (environments, formatted_error)
