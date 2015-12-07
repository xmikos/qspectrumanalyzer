# Maintainer: Michal Krenek (Mikos) <m.krenek@gmail.com>
pkgname=qspectrumanalyzer
pkgver=1.2.0
pkgrel=1
pkgdesc="Spectrum analyzer for RTL-SDR (GUI for rtl_power based on PyQtGraph)"
arch=('any')
url="https://github.com/xmikos/qspectrumanalyzer"
license=('GPL3')
depends=('python-pyqt4' 'python-pyqtgraph' 'rtl-sdr')
makedepends=('python-setuptools')
optdepends=('rtl_power_fftw-git: alternative rtl_power implementation using FFTW library')
source=(https://github.com/xmikos/qspectrumanalyzer/archive/v$pkgver.tar.gz)

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir"
}

# vim:set ts=2 sw=2 et:
