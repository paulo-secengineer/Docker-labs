Lab 13 - Docker ENTRYPOINT vs CMD
Practical tests on how Docker handles startup commands and argument overriding.


# Creating the script and setting permissions
vim hello.sh
chmod +x hello.sh

# Building the CMD image
docker build -t hello-cmd -f Dockerfile.cmd .

# Building the ENTRYPOINT image
docker build -t hello-entrypoint -f Dockerfile.entrypoint .

# Building the COMBO image (ENTRYPOINT + CMD)
docker build -t hello-combo -f Dockerfile.combo 


docker run hello-cmd sh -c 'echo "Another random command"'
# Output: Another random command.


docker run hello-entrypoint /bin/sh -c 'echo "trying to bypass entrypoint"'
# Output: Message: /bin/sh -c echo "trying to bypass entrypoint"


docker run hello-combo sh -c 'echo "it worked"'
# Output: Message: sh -c echo "it worked"

Key Takeaways:
CMD: A default value that can be easily "crushed" by the user.

ENTRYPOINT: The fixed command the container is born to execute.
