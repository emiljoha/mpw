flatpak-build:
	flatpak-builder build-dir se.emijoh.mpw.yml --force-clean

flatpak-install:
	flatpak-builder --user --install build-dir se.emijoh.mpw.yml --force-clean

flatpak-run:
	flatpak run se.emijoh.mpw


