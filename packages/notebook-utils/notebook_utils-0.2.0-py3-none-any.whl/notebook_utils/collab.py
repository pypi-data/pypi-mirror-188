
import importlib
def collab_install_git_dependencies(
    DEPENDENCIES,
) -> str:
    """Install dependencies in Google Collab.

    Example
    -------
    DEPENDENCIES=[
        ("name", "github.com/user/repo.git@RELEASE"),
        ("notebook_utils", f"github.com/sbland/notebook_utils/archive/main.zip"),
    ]
    """
    for name, path in DEPENDENCIES:
        try:
            importlib.import_module(name)
        except (ImportError, ModuleNotFoundError):
            if 'google.colab' in str(get_ipython()):
                try:
                    print('Running on CoLab')
                    print("""
                    This notebook requires access to private repositories. To access follow the steps below:
                    1. Get an access key from your github account: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
                    2. Save the key to a file in the following location on your google drive: `My Drive/access/collabaccess.txt`. The file should include your user on the first line and your token on the second.
                    """)
                    from google.colab import drive
                    drive.mount('/content/drive')

                    !mkdir -p ~/.access
                    !cp "/content/drive/My Drive/access/collabaccess.txt" ~/.access/config
                    import os
                    creds = open(f'{os.path.expanduser("~")}/.access/config')
                    creds_parsed = creds.read().splitlines()
                    user, token = creds_parsed

                    print(f"------ Installing {name}----------------")
                    try:
                        stdout = !pip install https://{user}:{token}@{path} --ignore-requires-python
                        if "Host key verification failed" in "\n".join(stdout):
                            print(f"------------- Failed to install with dependencies for {name} ---------------")
                            # If it fails to install try installing without dependencies
                            # git+ssh dependencies will currently fail
                            !pip install https://{user}:{token}@{path} --no-deps --ignore-requires-python
                    except:
                        print(f"Failed to install all of {name} at {path}")
                    finally:
                        print("\n".join(stdout))
                    creds.close()
                except:
                    print("=======FAILED TO INSTALL ADDTIONAL DEPENDENCIES!=======\nCheck instructions above")
    creds = None
    creds_parsed = None
    user = None
    token = None