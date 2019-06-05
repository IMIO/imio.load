let
  nixpkgs = builtins.fromJSON (builtins.readFile ./.nixpkgs-version.json);
  requirements = import ./requirements.nix { inherit pkgs; };
  pkgs = import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/${nixpkgs.rev}.tar.gz";
    inherit (nixpkgs) sha256;
}) {};
  cleanup = pkgs.callPackage ./default.nix {};
in
with import <nixpkgs> {};

pkgs.mkShell {
  buildInputs = [
    cleanup
    gitAndTools.pre-commit
    requirements.packages."locustio"
    requirements.packages."uncurl"
    zsh
  ];
}
