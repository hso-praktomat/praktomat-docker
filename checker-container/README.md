# Creating a checker container for safe-docker

You can find a Dockerfile template in this directory.
Modify it to your needs.
Generally, you need to install the packages you require.
Either through a package manager or manually.
You also might want to add some unit tests.
It's best to copy those into the image/container.
If those are not located within a subdirectory of the directory the Dockerfile is contained in, you need to go to one of the parent directories of the directory the unit tests are contained in.
Then build the image with something like this:

```
docker build -t aud-java . -f aud-material/praktikum-java/praktomat/Dockerfile
```

* Specify the image name in your environment file with the parameter `PRAKTOMAT_CHECKER_IMAGE`.
* `PRAKTOMAT_CHECKER_UID_MOD` prevents the UID and GID of the user executing the checks in the Docker container from being modified to match those of the user running Praktomat. Keep in mind that you might run your checkers as root (although it's just inside the container). It is determined by what you specify in your Dockerfile.
* `PRAKTOMAT_CHECKER_WRITABLE` can be used to make the filesystem of a container writable when running a checker. Otherwise, it's read-only. However, the directory containing the submission is always writable, regardless of this setting.

If you want to use CheckStyle, leave that line in the template as it is. Otherwise, it won't work with the way things are set up right now.
