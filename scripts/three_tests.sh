# Remember to setup the KIOKU_PATH environment variable to point to the root of the project.
# Script must obtain name of the file that contains lines.
if [ -z "$KIOKU_PATH" ]; then
    echo "KIOKU_PATH is not set. Please set it to the root of the project."
    exit 1
fi

if [ -z "$1" ]; then
    echo "Please provide the name of the file that contains lines. EXCLUDE THE .txt EXTENSION."
    exit 1
fi

python3 $KIOKU_PATH/test.py $1 --max=20 --correct=4