# Stop any currently-running instance
singularity instance stop iiif1

# Create the singularity instance
./startup.sh

# Activate the IIIF server inside the contianer
nohup singularity run --env VIPS_DISC_THRESHOLD=250m instance://iiif1 > iiif.log &

# Check that images are loading at https://printprobdb.psc.edu/books
# Logout of the shell