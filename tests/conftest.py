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
    """Real HTML structure from datos.gob.mx/dataset/expedientes_clasificados_ceav."""
    return """<!DOCTYPE html>
<html lang="es">
<body>
<div class="jumbotron jumbotron-fluid" style="height: 220px; width: 100%;">
  <div class="d-flex flex-column justify-content-center align-items-center text-white h-100">
    <h1 class="text-center jumbotron-title font-weight-bolder">
      Expedientes Clasificados CEAV
    </h1>
  </div>
</div>
<div class="main">
  <div id="content" class="container">
    <div class="row">
      <aside class="secondary col-md-4 px-2">
        <section id="organization-info" class="module module-narrow">
          <div class="module card custom-card mb-2 context-info">
            <div class="module-content">
              <div class="item-image-wrapper">
                <a href="/organization/ceav">
                  <img class="item-image" src="https://www.datos.gob.mx/uploads/group/2025-10-01-212937.316552LogoCEAV.png" alt="ceav">
                </a>
              </div>
              <h1 class="heading text-gold">Comisión Ejecutiva de Atención a Víctimas (CEAV)</h1>
              <p class="description">
                La Comisión Ejecutiva de Atención a Víctimas (CEAV) tiene como misión acompañar a las víctimas...
              </p>
              <p class="read-more"><a href="/organization/about/ceav">leer más</a></p>
            </div>
          </div>
        </section>
        <section class="module module-narrow module-shallow license">
          <h2 class="module-social-heading">Licencia</h2>
          <p class="module-content">
            <a href="https://creativecommons.org/licenses/by/4.0/" rel="dc:rights">Creative Commons Attribution 4.0</a>
          </p>
        </section>
      </aside>
      <div class="primary col-md-8 col-xs-12 px-2" role="main">
        <div class="notes embedded-content">
          <p>Expedientes que han sido clasificados como reservados por el Comité de Transparencia de la CEAV.</p>
        </div>
        <section id="dataset-resources" class="resources">
          <ul class="resource-list">
            <li class="resource-item card card-custom border-card mb-3" data-id="c4b5b5e1-86df-482e-aa5e-466bef5e777f">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/expedientes_clasificados_ceav/resource/c4b5b5e1-86df-482e-aa5e-466bef5e777f" title="Índice de Expedientes Clasificados como Reservados">
                      Índice de Expedientes Clasificados como Reservados
                    </a>
                  </h3>
                  <p class="mb-2">
                    Base de datos con el numero de expedientes que han sido clasificados como reservados por el Comité de Transparencia de la CEAV (actualizado en diciembre de 2025).
                  </p>
                  <p class="mb-2">
                    <strong>Categoría:</strong>
                    <a href="/group/seguridad">Seguridad</a>
                  </p>
                  <p class="mb-2">
                    <strong>Formatos:</strong>
                    <span class="text-center rounded font-weight-bold flex-shrink-0 mr-2 px-2 py-1 text-sm text-black" property="dc:format" data-format="csv" style="background-color: #E6D194;">
                      <span class="ml-1">CSV</span>
                    </span>
                  </p>
                  <p class="mb-0">
                    <strong>Institución:</strong>
                    <a class="link-pink" href="/organization/ceav">
                      Comisión Ejecutiva de Atención a Víctimas (CEAV)
                    </a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/expedientes_clasificados_ceav/resource/c4b5b5e1-86df-482e-aa5e-466bef5e777f" class="btn btn-primary">
                      Consultar
                    </a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/ceav/expedientes_clasificados_ceav/Expedientes_clasificados_CEAV.csv" class="btn btn-outline-primary">
                      <i class="fa fa-download"></i>
                      Descargar
                    </a>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </section>
        <section class="tags">
          <ul class="tag-list">
            <li><a class="tag" href="/dataset/?tags=acceso+informaci%C3%B3n" title="acceso información">acceso información</a></li>
            <li><a class="tag" href="/dataset/?tags=denuncias" title="denuncias">denuncias</a></li>
            <li><a class="tag" href="/dataset/?tags=derecho+informaci%C3%B3n" title="derecho información">derecho información</a></li>
            <li><a class="tag" href="/dataset/?tags=difusi%C3%B3n+informaci%C3%B3n" title="difusión información">difusión información</a></li>
            <li><a class="tag" href="/dataset/?tags=documentaci%C3%B3n" title="documentación">documentación</a></li>
            <li><a class="tag" href="/dataset/?tags=expediente" title="expediente">expediente</a></li>
            <li><a class="tag" href="/dataset/?tags=informaci%C3%B3n" title="información">información</a></li>
            <li><a class="tag" href="/dataset/?tags=inscritos" title="inscritos">inscritos</a></li>
            <li><a class="tag" href="/dataset/?tags=investigaci%C3%B3n" title="investigación">investigación</a></li>
            <li><a class="tag" href="/dataset/?tags=medio+informaci%C3%B3n" title="medio información">medio información</a></li>
            <li><a class="tag" href="/dataset/?tags=sistema+documental" title="sistema documental">sistema documental</a></li>
            <li><a class="tag" href="/dataset/?tags=transparencia" title="transparencia">transparencia</a></li>
            <li><a class="tag" href="/dataset/?tags=usuario+informaci%C3%B3n" title="usuario información">usuario información</a></li>
          </ul>
        </section>
        <section class="additional-info">
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr><th scope="col">Campo</th><th scope="col">Valor</th></tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row" class="dataset-label">Administrador</th>
                <td class="dataset-details" property="dc:contributor">Comisión Ejecutiva de Atención a Víctimas (CEAV)</td>
              </tr>
              <tr>
                <th scope="row" class="dataset-label">Última actualización</th>
                <td class="dataset-details">
                  <span class="automatic-local-datetime" data-datetime="2026-03-23T16:29:56+0000">23 de marzo de 2026, 10:29 (UTC-06:00)</span>
                </td>
              </tr>
              <tr>
                <th scope="row" class="dataset-label">Creado</th>
                <td class="dataset-details">
                  <span class="automatic-local-datetime" data-datetime="2026-03-23T16:28:17+0000">23 de marzo de 2026, 10:28 (UTC-06:00)</span>
                </td>
              </tr>
            </tbody>
          </table>
        </section>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""
