{ lib, ... }:
{

  flake.actions-nix = {
    pre-commit.enable = true;
    defaultValues = {
      jobs = {
        timeout-minutes = 60;
        runs-on = "ubuntu-latest";
      };
    };
    workflows =

      let
        checkoutStep = {
          uses = "actions/checkout@v4";
        };
        installNixStep = {
          uses = "DeterminateSystems/nix-installer-action@v9";
        };
        nixFlakeCheckNoBuildStep = {
          name = "Check flake";
          run = "nix -Lv flake check --no-build";
        };
        cachixStep = {
          uses = "cachix/cachix-action@v14";
          "with" = {
            name = "nialov";
          };
          continue-on-error = true;
        };
        nixFastBuildStep = {
          name = "Evaluate and build checks faster";
          run = "nix run .#nix-fast-build-ci";
        };
        uvSetupStep = {
          uses = "astral-sh/setup-uv@v6";
          "with" = {
            enable-cache = true;
          };
        };
        # From: https://github.com/pmgbergen/porepy/blob/develop/dockerfiles/base/Dockerfile
        installGmshDeps = {
          run = lib.concatStringsSep " && " [
            "sudo apt-get update"
            "sudo apt-get install -y build-essential libglu1-mesa libxrender1 libxcursor1 libxft2 libxinerama1 ffmpeg libsm6 libxext6"
          ];
        };
        uvInstall = {
          name = "Install dependencies";
          run = "uv sync";
        };
        uvTestImport = {
          name = "Test importing installed packages";
          run = "uv run python3 -c 'import fractopo; import porepy; import ogstools; import ogs'";
        };

        pipSetup = {
          uses = "actions/setup-python@v5";
          "with" = {
            python-version = "3.12";
            cache = "pip";
          };
        };
        pipInstall = {
          name = "Install dependencies";
          run = "pip install --requirement requirements.txt";
        };
        pipTestImport = {
          name = "Test importing installed packages";
          run = "python3 -c 'import fractopo; import porepy; import ogstools; import ogs'";
        };
        testScript = {
          name = "Test script";
          run = "python3 generate_fracture_parameters.py";
        };

      in
      {
        ".github/workflows/main.yaml" = {

          jobs = {
            "nix-check" = {
              steps = [
                checkoutStep
                installNixStep
                cachixStep
                installNixStep
                nixFlakeCheckNoBuildStep
                nixFastBuildStep
              ];
            };
            "uv-install-check" = {
              defaults.run.working-directory = "./fractopo_to_porepy_and_opengeosys/";
              steps = [
                checkoutStep
                installGmshDeps
                uvSetupStep
                uvInstall
                uvTestImport
                testScript
              ];
            };
            "pip-install-check" = {
              defaults.run.working-directory = "./fractopo_to_porepy_and_opengeosys/";
              steps = [
                checkoutStep
                installGmshDeps
                pipSetup
                pipInstall
                pipTestImport
                testScript
              ];
            };
          };

        };

      };
  };
}
