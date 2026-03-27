import pytest


@pytest.fixture
def datasets_page_1_html() -> str:
    return """<!DOCTYPE html>
<html>
<body>
<ul class="dataset-list list-unstyled">
  <li class="resource-item card card-custom border-card mb-3">
    <div class="row g-0">
      <div class="col p-3">
        <h3 class="mb-2">
          <a href="/dataset/incidencia_delictiva" class="text-black">Incidencia delictiva</a>
        </h3>
        <p class="mb-2"><strong>Última Actualización:</strong> 3 de marzo 2026</p>
        <p class="mb-2">Se muestran los hechos delictivos. <a href="/dataset/incidencia_delictiva" class="ms-1">Ver base de datos</a></p>
        <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
        <p class="mb-0"><strong>Institución:</strong> <a class="link-pink" href="/organization/sesnsp">SESNSP</a></p>
        <p class="mb-2"><strong>Número de bases de datos: 3</strong></p>
      </div>
    </div>
  </li>
  <li class="resource-item card card-custom border-card mb-3">
    <div class="row g-0">
      <div class="col p-3">
        <h3 class="mb-2">
          <a href="/dataset/bajas_personal" class="text-black">Bajas de personal</a>
        </h3>
        <p class="mb-2"><strong>Última Actualización:</strong> 12 de febrero 2026</p>
        <p class="mb-2">Registros de bajas de personal. <a href="/dataset/bajas_personal" class="ms-1">Ver base de datos</a></p>
        <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
        <p class="mb-0"><strong>Institución:</strong> <a class="link-pink" href="/organization/secretaria_marina">Secretaría de Marina (SEMAR)</a></p>
        <p class="mb-2"><strong>Número de bases de datos: 2</strong></p>
      </div>
    </div>
  </li>
</ul>
<div class="pagination-wrapper">
  <ul class="pagination">
    <li class="page-item active"><a class="page-link" href="/group/seguridad?page=1">1</a></li>
    <li class="page-item"><a class="page-link" href="/group/seguridad?page=2">2</a></li>
    <li class="page-item"><a class="page-link" href="/group/seguridad?page=2">»</a></li>
  </ul>
</div>
</body>
</html>"""


@pytest.fixture
def datasets_page_2_html() -> str:
    return """<!DOCTYPE html>
<html>
<body>
<ul class="dataset-list list-unstyled">
  <li class="resource-item card card-custom border-card mb-3">
    <div class="row g-0">
      <div class="col p-3">
        <h3 class="mb-2">
          <a href="/dataset/estadisticas_seguridad" class="text-black">Estadísticas de seguridad</a>
        </h3>
        <p class="mb-2"><strong>Última Actualización:</strong> 1 de enero 2026</p>
        <p class="mb-2">Estadísticas generales de seguridad pública. <a href="/dataset/estadisticas_seguridad" class="ms-1">Ver base de datos</a></p>
        <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
        <p class="mb-0"><strong>Institución:</strong> <a class="link-pink" href="/organization/sspc">SSPC</a></p>
        <p class="mb-2"><strong>Número de bases de datos: 5</strong></p>
      </div>
    </div>
  </li>
</ul>
<div class="pagination-wrapper">
  <ul class="pagination">
    <li class="page-item"><a class="page-link" href="/group/seguridad?page=1">«</a></li>
    <li class="page-item"><a class="page-link" href="/group/seguridad?page=1">1</a></li>
    <li class="page-item active"><a class="page-link" href="/group/seguridad?page=2">2</a></li>
  </ul>
</div>
</body>
</html>"""


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
