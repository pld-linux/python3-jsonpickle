#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Python library for serializing any arbitrary object graph into JSON
Summary(pl.UTF-8):	Biblioteka Pythona do serializacji dowolnego grafu obiektów do JSON-a
Name:		python3-jsonpickle
Version:	4.1.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jsonpickle/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonpickle/jsonpickle-%{version}.tar.gz
# Source0-md5:	39bec275ad39ebd3699f962dabd6cdf8
URL:		https://pypi.org/project/jsonpickle/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-toml
%if %{with tests}
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-ecdsa
BuildRequires:	python3-feedparser
BuildRequires:	python3-gmpy2
BuildRequires:	python3-numpy
BuildRequires:	python3-pandas
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black-multipy
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-flake8
# >= 1.1.1 when available
BuildRequires:	python3-scipy
# >= 1.9.3 for python 3.11+
BuildRequires:	python3-scikit-learn
BuildRequires:	python3-simplejson
BuildRequires:	python3-sqlalchemy >= 1.2.19
# TODO
#BuildRequires:	python3-bson
#BuildRequires:	python3-pymongo
#BuildRequires:	python3-ujson
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 3.2
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jsonpickle is a library for the two-way conversion of complex Python
objects and JSON. jsonpickle builds upon the existing JSON encoders,
such as simplejson, json.

%description -l pl.UTF-8
jsonpickle to biblioteka do dwustronnej konwersji między złożonymi
obiektami Pythona a JSON-em. jsonpickle jest zbudowany w oparciu o
istniejące kodery JSON-a, takie jak simplejson, json.

%package apidocs
Summary:	API documentation for Python jsonpickle module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jsonpickle
Group:		Documentation

%description apidocs
API documentation for Python jsonpickle module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jsonpickle.

%prep
%setup -q -n jsonpickle-%{version}

%{__sed} -i -e '/^norecursedirs/ s/$/ build-3/' pytest.ini

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black,pytest_cov.plugin,pytest_flake8" \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/jsonpickle
%{py3_sitescriptdir}/jsonpickle-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
