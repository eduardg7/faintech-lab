from setuptools import setup, find_packages

setup(
    name="meta-ai-memory",
    version="0.1.0",
    description="Persistent agent memory library for Faintech AI agents",
    author="Faintech Solutions SRL",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "agent-memory=src.memory.cli:main",
        ],
    },
)
