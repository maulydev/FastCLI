import click
import os
from pathlib import Path
import subprocess
import sys

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
    for filename in ["__init__.py", "models.py", "views.py", "services.py", "schemas.py", "urls.py"]:
        content = render_template(f"app/{filename}.tpl")
        create_file(app_path / filename, content)

    click.secho("✅ App created!", fg="green")



@main.command()
@click.option("--host", default="127.0.0.1", show_default=True, help="Host to run the server on.")
@click.option("--port", default=8000, show_default=True, help="Port to run the server on.")
@click.option("--reload/--no-reload", default=True, help="Enable automatic reload on code changes.")
def run(host, port, reload):
    """Run the FastAPI development server."""
    click.secho(f"\n🚀 Starting server at http://{host}:{port}/docs\n", fg="cyan", bold=True)
    
    # Determine entrypoint module: manage.py or project folder
    entry_script = Path("manage.py")
    if entry_script.exists():
        cmd = [sys.executable, "manage.py", "runserver", host, str(port)]
    else:
        # attempt to infer project_name from a directory containing settings.py
        proj_dirs = [p for p in Path(".").iterdir() if p.is_dir() and (p/"settings.py").exists()]
        if proj_dirs:
            module = proj_dirs[0].name + ".urls:app"
        else:
            module = "main:app"
        cmd = ["uvicorn", module, "--host", host, "--port", str(port)]
        if reload:
            cmd.append("--reload")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.secho(f"❌ Failed to start server: {e}", fg="red", err=True)

@main.command()
def install():
    """Install the most common FastAPI dependencies into the current environment."""
    deps = ["fastapi", "uvicorn", "pydantic", "sqlalchemy"]
    click.secho("\n📦 Installing dependencies...\n", fg="white", bold=True)

    for pkg in deps:
        click.secho(f" ➤ Installing {pkg}", fg="blue", nl=False)
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True, stdout=subprocess.DEVNULL)
            click.secho(" ✓", fg="green")
        except subprocess.CalledProcessError:
            click.secho(" ✗", fg="red")
    
    click.secho(" ➤ Freezing requirements...", fg="blue")
    
    with open("requirements.txt", "w") as f:
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f, check=True)
    
    click.secho("\n✅ All done! Start your server with: fast runserver\n", fg="green", bold=True)