import click
import os
from pathlib import Path
import subprocess

TEMPLATE_DIR = Path(__file__).parent / "templates"

def render_template(template_name, name=None):
    if name:
        return (TEMPLATE_DIR / template_name).read_text().replace("{{ project_name }}", name)
    return (TEMPLATE_DIR / template_name).read_text()

def create_file(path: Path, content: str):
    os.makedirs(path.parent, exist_ok=True)
    path.write_text(content)

@click.group()
def main():
    """🚀 FastCLI - Quickly Spin up FastAPI projects and apps."""
    pass

@main.command()
@click.argument("name")
@click.argument("dir", required=False)
@click.option('--with-docker', is_flag=True, help='Include Dockerfile and .dockerignore')
def startproject(name, dir, with_docker):
    """Create a new FastAPI project."""
    
    # Determine base path
    if dir in [None, ".", "./"]:
        base_path = Path(".").resolve()
    else:
        base_path = Path(dir).resolve()

    project_name = name
    app_path = base_path / project_name

    click.echo(f"🚀 Creating project '{project_name}' in {base_path}")

    # Create main files
    create_file(base_path / "manage.py", render_template("manage.py.tpl", project_name))
    create_file(app_path / "__init__.py", "")
    create_file(app_path / "settings.py", render_template("settings.py.tpl", project_name))
    create_file(app_path / "urls.py", render_template("urls.py.tpl", project_name))
    create_file(app_path / "database.py", render_template("database.py.tpl", project_name))

    # Git setup
    subprocess.run(["git", "init", str(base_path)])
    create_file(base_path / ".gitignore", render_template("gitignore.tpl", project_name))
    click.secho("🔧 Initialized Git repo", fg="magenta")

    # Docker support
    if with_docker:
        create_file(base_path / "Dockerfile", render_template("Dockerfile.tpl", project_name))
        create_file(base_path / ".dockerignore", render_template("dockerignore.tpl"))
        click.secho("🐳 Added Docker support", fg="blue")

    click.secho("✅ Project created!", fg="green")


@main.command()
@click.argument("name")
def startapp(name):
    """Create a new FastAPI app."""
    click.echo(f"📦 Creating app: {name}")
    app_path = Path(name)
    for filename in ["__init__.py", "models.py", "views.py", "serializers.py", "urls.py"]:
        content = render_template(f"app/{filename}.tpl")
        create_file(app_path / filename, content)

    click.secho("✅ App created!", fg="green")
