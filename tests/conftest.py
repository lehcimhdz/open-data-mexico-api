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


@pytest.fixture
def dataset_detail_html() -> str:
    return """<!DOCTYPE html>
<html>
<body>
<div class="jumbotron jumbotron-fluid">
  <div class="d-flex flex-column justify-content-center align-items-center text-white h-100">
    <h1 class="text-center jumbotron-title font-weight-bolder">Expedientes Clasificados CEAV</h1>
  </div>
</div>
<div class="main">
  <div id="content" class="container">
    <section id="organization-info" class="module module-narrow">
      <div class="module-content">
        <a href="/organization/ceav">
          <img class="item-image" src="https://www.datos.gob.mx/uploads/group/LogoCEAV.png" alt="ceav">
        </a>
        <h1 class="heading text-gold">Comisión Ejecutiva de Atención a Víctimas (CEAV)</h1>
        <p class="description">La CEAV tiene como misión acompañar a las víctimas.</p>
      </div>
    </section>
    <section class="license">
      <a href="https://creativecommons.org/licenses/by/4.0/" rel="dc:rights">Creative Commons Attribution 4.0</a>
    </section>
    <div class="notes embedded-content">
      <p>Expedientes que han sido clasificados como reservados por el Comité de Transparencia de la CEAV.</p>
    </div>
    <ul class="resource-list">
      <li class="resource-item card card-custom border-card mb-3" data-id="c4b5b5e1-86df-482e-aa5e-466bef5e777f">
        <div class="row g-0">
          <div class="col p-3">
            <h3 class="mb-2">
              <a class="text-black" href="/dataset/expedientes_clasificados_ceav/resource/c4b5b5e1-86df-482e-aa5e-466bef5e777f" title="Índice de Expedientes Clasificados como Reservados">
                Índice de Expedientes Clasificados como Reservados
              </a>
            </h3>
            <p class="mb-2">Base de datos con el numero de expedientes clasificados como reservados.</p>
            <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
            <p class="mb-2"><strong>Formatos:</strong>
              <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
            </p>
            <p class="mb-0"><strong>Institución:</strong>
              <a class="link-pink" href="/organization/ceav">Comisión Ejecutiva de Atención a Víctimas (CEAV)</a>
            </p>
            <div class="mt-4">
              <a href="/dataset/expedientes_clasificados_ceav/resource/c4b5b5e1-86df-482e-aa5e-466bef5e777f" class="btn btn-primary">Consultar</a>
              <a href="https://repodatos.atdt.gob.mx/api_update/ceav/expedientes_clasificados_ceav/Expedientes_clasificados_CEAV.csv" class="btn btn-outline-primary">Descargar</a>
            </div>
          </div>
        </div>
      </li>
    </ul>
    <ul class="tag-list">
      <li><a class="tag" href="/dataset/?tags=transparencia" title="transparencia">transparencia</a></li>
      <li><a class="tag" href="/dataset/?tags=expediente" title="expediente">expediente</a></li>
    </ul>
    <section class="additional-info">
      <table class="table">
        <tbody>
          <tr>
            <th>Administrador</th>
            <td>Comisión Ejecutiva de Atención a Víctimas (CEAV)</td>
          </tr>
          <tr>
            <th>Última actualización</th>
            <td><span class="automatic-local-datetime" data-datetime="2026-03-23T16:29:56+0000">23 de marzo de 2026</span></td>
          </tr>
          <tr>
            <th>Creado</th>
            <td><span class="automatic-local-datetime" data-datetime="2026-03-23T16:28:17+0000">23 de marzo de 2026</span></td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</div>
</body>
</html>"""
