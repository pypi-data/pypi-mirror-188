import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='BRIntel',
    version=0.1,
    author="VaultSec, Julio Lira, Matheus Oliveira",
    author_email="contato@vaultsec.com.br, jul10l1r4@disroot.org, matheusoliveiratux4me@gmail.com",
    description="Cyber Threat Intelligence (CTI) usando fontes e indicadores de ameaças nacionais, ou até globais, mas com evidencias ou indicadores nacionais do Brasil",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VaultSEC/BRIntelcollector",
    packages=["BRIntel", "BRIntel.xfe", "BRIntel.otx"],
    license="GPLv3",
    keywords="threat intelligence security ibm xforce x-force blueteam search query api exchange otx cti oct OTX otx open threat CTI brazil brasil br",
    project_urls={
        'Vault Cyber Security': 'https://vaultsec.com.br/',
        'Github profile': 'https://github.com/VaultSEC'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Security",
        ],
    )

