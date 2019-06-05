{ pkgs ? import <nixpkgs> {} }:
let
  requirements = import ./requirements.nix { inherit pkgs; };
in
pkgs.python37Packages.buildPythonPackage rec {
  name = "imio-load";
  version = "0.1.0";
  namePrefix = "";
  src = pkgs.nix-gitignore.gitignoreSource [] ./.;
  doCheck = false;
  propagatedBuildInputs = [
    requirements.packages."locustio"
    requirements.packages."lxml"
    requirements.packages."uncurl"
];
  buildInputs = propagatedBuildInputs;
}
