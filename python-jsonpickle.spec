#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python library for serializing any arbitrary object graph into JSON
Summary(pl.UTF-8):	Biblioteka Pythona do serializacji dowolnego grafu obiektów do JSON-a
Name:		python-jsonpickle
Version:	2.0.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jsonpickle/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonpickle/jsonpickle-%{version}.tar.gz
# Source0-md5:	ed497bb9c2963ba3584ef6ae3454cc13
URL:		https://pypi.org/project/jsonpickle/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 3.4.1
BuildRequires:	python-toml
%if %{with tests}
BuildRequires:	python-ecdsa
BuildRequires:	python-importlib_metadata
BuildRequires:	python-numpy
BuildRequires:	python-pandas
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-black-multipy
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-flake8
BuildRequires:	python-scikit-learn
BuildRequires:	python-simplejson
BuildRequires:	python-sqlalchemy
# TODO
#BuildRequires:	python-bson
#BuildRequires:	python-demjson
#BuildRequires:	python-feedparser
#BuildRequires:	python-ujson
#BuildRequires:	python-yajl
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-ecdsa
BuildRequires:	python3-numpy
BuildRequires:	python3-pandas
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black-multipy
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-scikit-learn
BuildRequires:	python3-simplejson
BuildRequires:	python3-sqlalchemy
# TODO
#BuildRequires:	python3-bson
#BuildRequires:	python3-demjson
#BuildRequires:	python3-feedparser
#BuildRequires:	python3-ujson
#BuildRequires:	python3-yajl
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-jaraco.packaging
BuildRequires:	python3-rst.linker
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jsonpickle is a library for the two-way conversion of complex Python
objects and JSON. jsonpickle builds upon the existing JSON encoders,
such as simplejson, json, and demjson.

%description -l pl.UTF-8
jsonpickle to biblioteka do dwustronnej konwersji między złożonymi
obiektami Pythona a JSON-em. jsonpickle jest zbudowany w oparciu o
istniejące kodery JSON-a, takie jak simplejson, json i demjson.

%package -n python3-jsonpickle
Summary:	Python library for serializing any arbitrary object graph into JSON
Summary(pl.UTF-8):	Biblioteka Pythona do serializacji dowolnego grafu obiektów do JSON-a
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-jsonpickle
jsonpickle is a library for the two-way conversion of complex Python
objects and JSON. jsonpickle builds upon the existing JSON encoders,
such as simplejson, json, and demjson.

%description -n python3-jsonpickle -l pl.UTF-8
jsonpickle to biblioteka do dwustronnej konwersji między złożonymi
obiektami Pythona a JSON-em. jsonpickle jest zbudowany w oparciu o
istniejące kodery JSON-a, takie jak simplejson, json i demjson.

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

%{__sed} -i -e '/^norecursedirs/ s/$/ build-2 build-3/' pytest.ini

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_dict_self_cycle has result just like python3 (not python2) expected value(?)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black_multipy,pytest_cov.plugin,pytest_flake8" \
%{__python} -m pytest tests -k 'not test_dict_self_cycle'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black,pytest_cov.plugin,pytest_flake8" \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/jsonpickle
%{py_sitescriptdir}/jsonpickle-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jsonpickle
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/jsonpickle
%{py3_sitescriptdir}/jsonpickle-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
