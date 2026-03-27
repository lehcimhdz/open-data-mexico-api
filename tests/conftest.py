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


@pytest.fixture
def dataset_detail_prs_html() -> str:
    """Real HTML structure from datos.gob.mx/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026.

    This dataset has 36 resources; the fixture retains 3 representative ones
    plus the first and last to keep it concise while exercising multi-resource parsing.
    """
    return """<!DOCTYPE html>
<html lang="es">
<body>
<div class="jumbotron jumbotron-fluid" style="height: 220px; width: 100%;">
  <div class="d-flex flex-column justify-content-center align-items-center text-white h-100">
    <h1 class="text-center jumbotron-title font-weight-bolder">
      Cuaderno Mensual Estadístico Penitenciario (enero, 2026)
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
                <a href="/organization/prs">
                  <img class="item-image" src="https://www.datos.gob.mx/uploads/group/2025-04-14-223907.623075LogoPRSpng.png" alt="prs">
                </a>
              </div>
              <h1 class="heading text-gold">Prevención y Reinserción Social (PRS)</h1>
              <p class="description">
                Instrumenta la política penitenciaria a nivel nacional...
              </p>
              <p class="read-more"><a href="/organization/about/prs">leer más</a></p>
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
          <p>Datos de la población privada de la libertad en entidades federativas y Centros Penitenciarios Federales.</p>
        </div>
        <section id="dataset-resources" class="resources">
          <ul class="resource-list">

            <li class="resource-item card card-custom border-card mb-3" data-id="ba313dc7-391b-4900-9ec2-a475b5e46443">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026/resource/ba313dc7-391b-4900-9ec2-a475b5e46443" title="Estadística penitenciaria: espacios, población y sobrepoblación por fuero, situación jurídica y sexo">
                      Estadística penitenciaria: espacios, población...
                    </a>
                  </h3>
                  <p class="mb-2">
                    Espacios, sobrepoblación y población privada de la libertad según fuero, situación jurídica y sexo por entidad federativa y Centro Penitenciario Federal.
                  </p>
                  <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
                  <p class="mb-2"><strong>Formatos:</strong>
                    <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
                  </p>
                  <p class="mb-0"><strong>Institución:</strong>
                    <a class="link-pink" href="/organization/prs">Prevención y Reinserción Social (PRS)</a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026/resource/ba313dc7-391b-4900-9ec2-a475b5e46443" class="btn btn-primary">Consultar</a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/prs/cuaderno_mensual_estadistico_penitenciario_enero_2026/fue_sjur_sex_centro1_ene26.csv" class="btn btn-outline-primary">Descargar</a>
                  </div>
                </div>
              </div>
            </li>

            <li class="resource-item card card-custom border-card mb-3" data-id="29c22724-a7ad-4d44-a11c-1a305111c6c2">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026/resource/29c22724-a7ad-4d44-a11c-1a305111c6c2" title="Estadística penitenciaria: centros, población y sobrepoblación por entidad y centro">
                      Estadística penitenciaria: centros, población...
                    </a>
                  </h3>
                  <p class="mb-2">
                    Número de centros penitenciarios, espacios, población privada de la libertad y sobrepoblación por entidad federativa y Centro Penitenciario Federal.
                  </p>
                  <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
                  <p class="mb-2"><strong>Formatos:</strong>
                    <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
                  </p>
                  <p class="mb-0"><strong>Institución:</strong>
                    <a class="link-pink" href="/organization/prs">Prevención y Reinserción Social (PRS)</a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026/resource/29c22724-a7ad-4d44-a11c-1a305111c6c2" class="btn btn-primary">Consultar</a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/prs/cuaderno_mensual_estadistico_penitenciario_enero_2026/sobrepob_ent_ene26.csv" class="btn btn-outline-primary">Descargar</a>
                  </div>
                </div>
              </div>
            </li>

            <li class="resource-item card card-custom border-card mb-3" data-id="aec4234c-ceaf-4551-a76d-9981235f8332">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026/resource/aec4234c-ceaf-4551-a76d-9981235f8332" title="Población penitenciaria indígena según fuero, situación jurídica y sexo por lengua">
                      Población penitenciaria indígena según fuero,...
                    </a>
                  </h3>
                  <p class="mb-2">
                    Población indígena privada de la libertad según fuero, situación jurídica y sexo por lengua indígena.
                  </p>
                  <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
                  <p class="mb-2"><strong>Formatos:</strong>
                    <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
                  </p>
                  <p class="mb-0"><strong>Institución:</strong>
                    <a class="link-pink" href="/organization/prs">Prevención y Reinserción Social (PRS)</a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/cuaderno_mensual_estadistico_penitenciario_enero_2026/resource/aec4234c-ceaf-4551-a76d-9981235f8332" class="btn btn-primary">Consultar</a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/prs/cuaderno_mensual_estadistico_penitenciario_enero_2026/ind_leng_fue_sjur_sexo_ene26.csv" class="btn btn-outline-primary">Descargar</a>
                  </div>
                </div>
              </div>
            </li>

          </ul>
        </section>
        <section class="tags">
          <ul class="tag-list">
            <li><a class="tag" href="/dataset/?tags=administraci%C3%B3n+justicia" title="administración justicia">administración justicia</a></li>
            <li><a class="tag" href="/dataset/?tags=centro+penitenciario" title="centro penitenciario">centro penitenciario</a></li>
            <li><a class="tag" href="/dataset/?tags=c%C3%A1rcel" title="cárcel">cárcel</a></li>
            <li><a class="tag" href="/dataset/?tags=delito" title="delito">delito</a></li>
            <li><a class="tag" href="/dataset/?tags=incidencia+delictiva" title="incidencia delictiva">incidencia delictiva</a></li>
            <li><a class="tag" href="/dataset/?tags=prisionero" title="prisionero">prisionero</a></li>
            <li><a class="tag" href="/dataset/?tags=prisi%C3%B3n" title="prisión">prisión</a></li>
            <li><a class="tag" href="/dataset/?tags=procedimiento+penal" title="procedimiento penal">procedimiento penal</a></li>
            <li><a class="tag" href="/dataset/?tags=sanci%C3%B3n+penal" title="sanción penal">sanción penal</a></li>
            <li><a class="tag" href="/dataset/?tags=sentencia" title="sentencia">sentencia</a></li>
            <li><a class="tag" href="/dataset/?tags=sistema+judicial" title="sistema judicial">sistema judicial</a></li>
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
                <td class="dataset-details" property="dc:contributor">Prevención y Reinserción Social (PRS)</td>
              </tr>
              <tr>
                <th scope="row" class="dataset-label">Última actualización</th>
                <td class="dataset-details">
                  <span class="automatic-local-datetime" data-datetime="2026-03-10T17:11:45+0000">10 de marzo de 2026, 11:11 (UTC-06:00)</span>
                </td>
              </tr>
              <tr>
                <th scope="row" class="dataset-label">Creado</th>
                <td class="dataset-details">
                  <span class="automatic-local-datetime" data-datetime="2026-03-09T21:40:15+0000">9 de marzo de 2026, 15:40 (UTC-06:00)</span>
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


@pytest.fixture
def dataset_detail_sesnsp_html() -> str:
    """Real HTML structure from datos.gob.mx/dataset/incidencia_delictiva.

    Notable: first resource uses 'Visualizar' instead of 'Consultar' on the
    primary button — detail_url must still be extracted from the h3 link.
    """
    return """<!DOCTYPE html>
<html lang="es">
<body>
<div class="jumbotron jumbotron-fluid" style="height: 220px; width: 100%;">
  <div class="d-flex flex-column justify-content-center align-items-center text-white h-100">
    <h1 class="text-center jumbotron-title font-weight-bolder">
      Incidencia delictiva
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
                <a href="/organization/sesnsp">
                  <img class="item-image" src="https://www.datos.gob.mx/uploads/group/LogoSESNSP.png" alt="sesnsp">
                </a>
              </div>
              <h1 class="heading text-gold">Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)</h1>
              <p class="description">Es un Órgano Administrativo Desconcentrado de la Secretaría de Gobernación...</p>
              <p class="read-more"><a href="/organization/about/sesnsp">leer más</a></p>
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
          <p>Se muestran los hechos delictivos, así como los diferentes tipos de delito, ocurridos entre 2015 y diciembre de 2025.</p>
        </div>
        <section id="dataset-resources" class="resources">
          <ul class="resource-list">

            <li class="resource-item card card-custom border-card mb-3" data-id="d9b2792a-33a2-4ea8-8527-210d9e99de5e">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/incidencia_delictiva/resource/d9b2792a-33a2-4ea8-8527-210d9e99de5e" title="Incidencia delictiva estatal">
                      Incidencia delictiva estatal
                    </a>
                  </h3>
                  <p class="mb-2">Se muestran los hechos delictivos ocurridos entre 2015 y diciembre 2025, en desagregación estatal.</p>
                  <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
                  <p class="mb-2"><strong>Formatos:</strong>
                    <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
                  </p>
                  <p class="mb-0"><strong>Institución:</strong>
                    <a class="link-pink" href="/organization/sesnsp">Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)</a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/incidencia_delictiva/resource/d9b2792a-33a2-4ea8-8527-210d9e99de5e" class="btn btn-primary">Visualizar</a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_dic25.csv" class="btn btn-outline-primary">Descargar</a>
                  </div>
                </div>
              </div>
            </li>

            <li class="resource-item card card-custom border-card mb-3" data-id="57fbd692-3e5c-4b1b-8621-694cb3a33035">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/incidencia_delictiva/resource/57fbd692-3e5c-4b1b-8621-694cb3a33035" title="Incidencia delictiva municipal">
                      Incidencia delictiva municipal
                    </a>
                  </h3>
                  <p class="mb-2">Se muestran los hechos delictivos ocurridos entre 2015 y diciembre de 2025, en desagregación municipal.</p>
                  <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
                  <p class="mb-2"><strong>Formatos:</strong>
                    <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
                  </p>
                  <p class="mb-0"><strong>Institución:</strong>
                    <a class="link-pink" href="/organization/sesnsp">Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)</a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/incidencia_delictiva/resource/57fbd692-3e5c-4b1b-8621-694cb3a33035" class="btn btn-primary">Consultar</a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/IDM_NM_dic25.csv" class="btn btn-outline-primary">Descargar</a>
                  </div>
                </div>
              </div>
            </li>

            <li class="resource-item card card-custom border-card mb-3" data-id="386f17d2-a488-4da2-9c85-99765b5a9cdc">
              <div class="row g-0">
                <div class="col-auto d-flex align-items-start p-3">
                  <img class="image-fluid" style="max-width: 60px;" src="https://www.datos.gob.mx/uploads/group/seguridad.svg" alt="">
                </div>
                <div class="col p-3">
                  <h3 class="mb-2">
                    <a class="text-black" href="/dataset/incidencia_delictiva/resource/386f17d2-a488-4da2-9c85-99765b5a9cdc" title="Víctimas del fuero común">
                      Víctimas del fuero común
                    </a>
                  </h3>
                  <p class="mb-2">Se muestran los datos de las víctimas de hechos delictivos ocurridos entre 2015 y diciembre de 2025, en desagregación estatal, por sexo y rango de edad.</p>
                  <p class="mb-2"><strong>Categoría:</strong> <a href="/group/seguridad">Seguridad</a></p>
                  <p class="mb-2"><strong>Formatos:</strong>
                    <span class="text-center rounded" property="dc:format" data-format="csv"><span class="ml-1">CSV</span></span>
                  </p>
                  <p class="mb-0"><strong>Institución:</strong>
                    <a class="link-pink" href="/organization/sesnsp">Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)</a>
                  </p>
                  <div class="mt-4">
                    <a href="/dataset/incidencia_delictiva/resource/386f17d2-a488-4da2-9c85-99765b5a9cdc" class="btn btn-primary">Consultar</a>
                    <a href="https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/IDVFC_NM_dic25.csv" class="btn btn-outline-primary">Descargar</a>
                  </div>
                </div>
              </div>
            </li>

          </ul>
        </section>
        <section class="tags">
          <ul class="tag-list">
            <li><a class="tag" href="/dataset/?tags=Arma+fuego" title="Arma fuego">Arma fuego</a></li>
            <li><a class="tag" href="/dataset/?tags=Carpetas" title="Carpetas">Carpetas</a></li>
            <li><a class="tag" href="/dataset/?tags=Delito" title="Delito">Delito</a></li>
            <li><a class="tag" href="/dataset/?tags=Extorsi%C3%B3n" title="Extorsión">Extorsión</a></li>
            <li><a class="tag" href="/dataset/?tags=Feminicidio" title="Feminicidio">Feminicidio</a></li>
            <li><a class="tag" href="/dataset/?tags=Homicidio+doloso" title="Homicidio doloso">Homicidio doloso</a></li>
            <li><a class="tag" href="/dataset/?tags=Lesi%C3%B3n+dolosa" title="Lesión dolosa">Lesión dolosa</a></li>
            <li><a class="tag" href="/dataset/?tags=Robo" title="Robo">Robo</a></li>
            <li><a class="tag" href="/dataset/?tags=Secuestro" title="Secuestro">Secuestro</a></li>
            <li><a class="tag" href="/dataset/?tags=Violaci%C3%B3n" title="Violación">Violación</a></li>
            <li><a class="tag" href="/dataset/?tags=Violencia" title="Violencia">Violencia</a></li>
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
                <td class="dataset-details" property="dc:contributor">Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)</td>
              </tr>
              <tr>
                <th scope="row" class="dataset-label">Última actualización</th>
                <td class="dataset-details">
                  <span class="automatic-local-datetime" data-datetime="2026-03-03T22:09:46+0000">3 de marzo de 2026, 16:09 (UTC-06:00)</span>
                </td>
              </tr>
              <tr>
                <th scope="row" class="dataset-label">Creado</th>
                <td class="dataset-details">
                  <span class="automatic-local-datetime" data-datetime="2025-03-13T23:27:31+0000">13 de marzo de 2025, 17:27 (UTC-06:00)</span>
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
