# Lil histie  

This repo contains an almost pointless python library to create histograms in the terminal from `gdalinfo` output. 

## Overview

We all know and love the GDAL utility command `gdalinfo`. Lil' histe displays the `gdalinfo` histogram objects calculated for each band. To use, pipe `gdalinfo` output with the `-json` option to lil_histie like so:  

```zsh
gdalinfo -hist input.tif -json | lil_histie
```  

And enjoy the little histograms printed in the terminal.