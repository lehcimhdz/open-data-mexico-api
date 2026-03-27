import pytest


@pytest.fixture
def categories_page_1_html() -> str:
    return """
<!DOCTYPE html>
<html>
<body>
<ul class="media-grid">
  <li class="media-item">
    <div class="item-image-wrapper">
      <img src="https://www.datos.gob.mx/uploads/group/agricultura.svg" alt="agricultura" class="media-image img-fluid">
    </div>
    <h2 class="media-heading">Agricultura</h2>
    <p class="media-description">Datos sobre la actividad agrícola en México.</p>
    <span class="count">139 Bases de Datos</span>
    <a href="/group/agricultura" title="Ver Agricultura" class="media-view"><span>Ver Agricultura</span></a>
  </li>
  <li class="media-item">
    <div class="item-image-wrapper">
      <img src="https://www.datos.gob.mx/uploads/group/educacion.svg" alt="educacion" class="media-image img-fluid">
    </div>
    <h2 class="media-heading">Educación</h2>
    <p class="media-description">Datos sobre el sistema educativo nacional.</p>
    <span class="count">1,204 Bases de Datos</span>
    <a href="/group/educacion" title="Ver Educación" class="media-view"><span>Ver Educación</span></a>
  </li>
</ul>
<div class="pagination-wrapper">
  <ul class="pagination">
    <li class="page-item active"><a class="page-link" href="/group/?page=1">1</a></li>
    <li class="page-item"><a class="page-link" href="/group/?page=2">2</a></li>
    <li class="page-item"><a class="page-link" href="/group/?page=2">»</a></li>
  </ul>
</div>
</body>
</html>
"""


@pytest.fixture
def categories_page_2_html() -> str:
    return """
<!DOCTYPE html>
<html>
<body>
<ul class="media-grid">
  <li class="media-item">
    <div class="item-image-wrapper">
      <img src="/uploads/group/salud.svg" alt="salud" class="media-image img-fluid">
    </div>
    <h2 class="media-heading">Salud</h2>
    <p class="media-description">Datos sobre salud pública y servicios médicos.</p>
    <span class="count">87 Bases de Datos</span>
    <a href="/group/salud" title="Ver Salud" class="media-view"><span>Ver Salud</span></a>
  </li>
</ul>
<div class="pagination-wrapper">
  <ul class="pagination">
    <li class="page-item"><a class="page-link" href="/group/?page=1">«</a></li>
    <li class="page-item"><a class="page-link" href="/group/?page=1">1</a></li>
    <li class="page-item active"><a class="page-link" href="/group/?page=2">2</a></li>
  </ul>
</div>
</body>
</html>
"""
