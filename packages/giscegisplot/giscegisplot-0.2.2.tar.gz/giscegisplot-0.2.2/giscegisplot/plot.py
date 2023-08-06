import geotiler
import tempfile
from descartes import PolygonPatch
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely import wkt
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import click
import sys


@click.group()
def giscegisplot():
    pass


@giscegisplot.command()
@click.option('--postgres_host', required=True)
@click.option('--postgres_port', type=int, default=5432)
@click.option('--postgres_database', required=True)
@click.option('--postgres_user', required=True)
@click.option('--postgres_password', required=True)
@click.option('--cpid', type=int, required=True)
@click.option('--mode', type=click.Choice(['tram', 'vano'], case_sensitive=False), default='tram')
def get_plot(postgres_host, postgres_port, postgres_database, postgres_user,
             postgres_password, cpid, mode):
    # DB Query
    con = psycopg2.connect(host=postgres_host, port=postgres_port, user=postgres_user,
                           dbname=postgres_database, password=postgres_password)
    cursor = con.cursor()
    if mode == 'vano':
        sql = """
                select
                    st_astext(st_transform(t.geom,4326)) as tram,
                    st_astext(st_transform(cp.geom,4326)) as parcela,
                    st_astext(st_centroid(st_transform(cp.geom,4326))) as centroid,
                    cp.name as name
                    from giscedata_parcela_vano_rel ptrel
                    join giscegis_catastre_parceles cp on cp.id = ptrel.parcela_id
                    join giscedata_at_vano t on t.id = ptrel.vano_id
                    where cp.id = %(cpid)s;
            """
    else:
        sql = """
                select
                    st_astext(st_transform(t.geom,4326)) as tram,
                    st_astext(st_transform(cp.geom,4326)) as parcela,
                    st_astext(st_centroid(st_transform(cp.geom,4326))) as centroid,
                    cp.name as name
                    from giscedata_parcela_tram_rel ptrel
                    join giscegis_catastre_parceles cp on cp.id = ptrel.parcela_id
                    join giscedata_at_tram t on t.id = ptrel.tram_id
                    where cp.id = %(cpid)s;
            """
    cursor.execute(sql, {"cpid": cpid})
    rows = cursor.fetchall()
    cursor.close()
    con.close()

    # mp 1 - n tram, we only need the first multipolygon (geom, centroid and title)
    # given a specific id
    trams = []
    mp = MultiPolygon(wkt.loads(rows[0][1]))
    centroid = Point(wkt.loads(rows[0][2]))
    title = rows[0][3]
    for row in rows:
        trams.append(LineString(wkt.loads(row[0])))


    minx, miny, maxx, maxy = mp.buffer(0.00035).bounds
    bbox = minx, miny, maxx, maxy
    
    # Try to fix User Agent to avoid Too Many Requests
    geotiler.io.HEADERS.update({
        'User-Agent': 'GISCE-{}-{}'.format(postgres_database, geotiler.io.HEADERS['User-Agent'])
    })

    # Geotiler map
    # mm = geotiler.Map(center=(centroid.x, centroid.y), zoom=16, size=(200, 200))

    # ZOOM IS A FIXED VALUE
    mm = geotiler.Map(extent=bbox, zoom=18)
    img = geotiler.render_map(mm)
    ax = plt.subplot(111)

    polygons = []

    # Plot mp
    for pol in mp:
        f_exterior = []
        f_interior = []

        for coord in pol.exterior.coords:
            f_exterior.append(mm.rev_geocode(coord))

        for interior in pol.interiors:
            hole = []
            for coord in interior.coords:
                hole.append(mm.rev_geocode(coord))
            f_interior.append(hole)

        polygons.append(Polygon(shell=f_exterior, holes=f_interior))

    vanos=[]

    for tram in trams:
        f_exterior = []
        dilated = tram.buffer(0.00007)
        for coord in dilated.exterior.coords:
            f_exterior.append(mm.rev_geocode(coord))
        vanos.append(Polygon(shell=f_exterior))
        # Plot line
        points = []
        x, y = tram.xy
        for i, element in enumerate(x):
            points.append((x[i], y[i]))
        x, y = zip(*(mm.rev_geocode(p) for p in points))
        ax.plot(x, y, color='red', alpha=0.7,
                linewidth=3, solid_capstyle='round', zorder=1)

    # Show geotiler map
    ax.imshow(img)

    # Plot title and remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title("Parcela " + str(title))

    patches_pol = []

    for idx, p in enumerate(polygons):
        patches_pol.append(PolygonPatch(p, alpha=1., zorder=2))
        ax.add_collection(
            PatchCollection(patches_pol, hatch='.....', color='SkyBlue', lw=.3,
                            edgecolor='blue'))
        for v in vanos:
            patches_lin = []
            patches_lin.append(PolygonPatch(v, alpha=1., zorder=1))
            ax.add_collection(
                PatchCollection(patches_lin, hatch='.....', color='PaleGreen',
                                lw=.3, edgecolor='green'))

    # Save plot
    # plt.savefig(cpid + '.png')
    tile_path = tempfile.mkstemp(prefix='tile-', suffix='.png')[1]
    plt.savefig(tile_path)
    sys.stdout.write(tile_path)
    sys.stdout.flush()
