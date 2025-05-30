{
  description = "Description for the project";

  inputs = {
    nix-extra = {
      url = "github:nialov/nix-extra";
    };
    nixpkgs.follows = "nix-extra/nixpkgs";
    flake-parts.follows = "nix-extra/flake-parts";
    actions-nix.url = "github:nialov/actions.nix";
  };

  outputs =
    inputs:
    let
      flakePart = inputs.flake-parts.lib.mkFlake { inherit inputs; } (
        {
          inputs,
          self,
          options,
          ...
        }:
        {
          systems = [ "x86_64-linux" ];
          imports = [
            inputs.nix-extra.flakeModules.custom-git-hooks
            inputs.actions-nix.flakeModules.default
            ./per-system.nix
            ./nix/ci.nix
          ];
          flake.self = self;
          flake.flakeOptions = options;
        }
      );

    in
    flakePart;

}
