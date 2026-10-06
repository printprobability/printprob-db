// Decode damaged-type matching run folders (written by shared/books/code/run_matching.sh on Bridges) into
// human-readable descriptions for Character Matches Review. Folder names look like
//   matching_output_<queries>-<start>-<end>_<candidates>.csv_q<q>c<c>_<YYYY-MM-DD>_<HH:MM:SS>
// e.g. matching_output_manualfortysermons-457-585_religionandreason.csv_q1.0c0.30_2026-10-06_07:08:09

// Slugs used in query/candidate names so far; anything else is shown as-is.
const BOOK_NAMES = {
  fortysermons: 'Forty Sermons',
  religionandreason: 'Religion and Reason',
  spinoza: 'Spinoza TTP',
  locke: 'Locke, Two Treatises',
  lockeletter: 'Locke, Letter on Toleration',
  plutarch: 'Plutarch',
  criticalenquiries: 'Critical Enquiries',
  tbraddyll: 'Braddyll books',
  everingham: 'Everingham books',
  everingham_english: 'Everingham English books',
  everingham_english_redo: 'Everingham English books',
  // title slugs from image folder names (<printer>_<ESTC>_<library>_<format>_<titleslug><year>)
  spinozatheologicalpolitical: 'Spinoza TTP',
  twotreatisesofgov: 'Locke, Two Treatises',
  Lockeletterconcerningtoler: 'Locke, Letter on Toleration',
  criticalenquiriesinto: 'Critical Enquiries',
  plutarchmorals: 'Plutarch, Morals',
}

const MONTHS = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
]

const DATE_ONLY_PATTERN =
  /^matching_output_(\d{4})-(\d{2})-(\d{2})_(\d{2}):(\d{2}):(\d{2})$/

// 2022 runs that recorded only the candidate list
const CANDIDATES_ONLY_PATTERN =
  /^matching_output_(.+)\.csv_(\d{4})-(\d{2})-(\d{2})_(\d{2}):(\d{2}):(\d{2})$/

const RUN_PATTERN =
  /^matching_output_(.+)-(\d+)-(\d+)_(.+)\.csv_q([\d.]+)c([\d.]+)_(\d{4})-(\d{2})-(\d{2})_(\d{2}):(\d{2}):(\d{2})$/

export function bookName(slug) {
  return BOOK_NAMES[slug] || slug
}

function percent(fraction) {
  return `${Math.round(parseFloat(fraction) * 100)}%`
}

// Returns null when the name doesn't follow the pattern; callers then show the raw folder name.
export function parseMatchDir(name) {
  const d = DATE_ONLY_PATTERN.exec(name)
  if (d) {
    // early (2022) runs were named by date only
    return {
      raw: name,
      dateOnly: true,
      date: `${parseInt(d[3])} ${MONTHS[parseInt(d[2]) - 1]} ${d[1]}`,
      time: `${d[4]}:${d[5]}`,
    }
  }
  const m = RUN_PATTERN.exec(name)
  if (!m) {
    const k = CANDIDATES_ONLY_PATTERN.exec(name)
    if (!k) return null
    return {
      raw: name,
      dateOnly: true,
      candidates: bookName(k[1]),
      date: `${parseInt(k[4])} ${MONTHS[parseInt(k[3]) - 1]} ${k[2]}`,
      time: `${k[5]}:${k[6]}`,
    }
  }
  const [, queries, start, end, candidates, q, c, yyyy, mm, dd, hh, min] = m
  let querySource, queryBook
  if (queries === 'autoqueries') {
    querySource = 'auto'
  } else if (queries.startsWith('manual')) {
    querySource = 'hand-picked'
    queryBook = queries.slice('manual'.length)
  } else if (queries.startsWith('viztargets')) {
    querySource = 'targeted'
    queryBook = queries.slice('viztargets'.length)
  } else {
    querySource = queries
  }
  return {
    raw: name,
    querySource,
    queryBook: queryBook ? bookName(queryBook) : null,
    pageStart: parseInt(start),
    pageEnd: parseInt(end),
    allPages: parseInt(start) === 0 && parseInt(end) >= 10000,
    candidates: bookName(candidates),
    q,
    c,
    date: `${parseInt(dd)} ${MONTHS[parseInt(mm) - 1]} ${yyyy}`,
    time: `${hh}:${min}`,
  }
}

function pagesText(run) {
  // page ranges are image indices, half-open [start, end)
  return run.allPages ? 'all pages' : `pp. ${run.pageStart}–${run.pageEnd - 1}`
}

function candidatesText(run) {
  return parseFloat(run.c) >= 1
    ? 'all candidates'
    : `top ${percent(run.c)} of candidates`
}

function queriesText(run) {
  if (run.querySource === 'auto') return `auto: most-damaged ${percent(run.q)}`
  if (run.querySource === 'targeted')
    return 'targeted: all glyphs on known-match pages'
  return run.querySource
}

// One line for the run selector.
export function describeRunShort(run, queryBookTitle) {
  if (!run) return null
  if (run.dateOnly) {
    return run.candidates
      ? `→ ${run.candidates} · ${run.date} ${run.time} (queries not recorded in the folder name)`
      : `Run of ${run.date} ${run.time} (parameters not recorded in the folder name)`
  }
  const book = run.queryBook || queryBookTitle || 'Query book'
  return `${book} ${pagesText(run)} (${queriesText(run)}) → ${
    run.candidates
  } · ${candidatesText(run)} · ${run.date} ${run.time}`
}

// Sentences for the "Now viewing" card.
export function describeRunLong(run, queryBookTitle) {
  if (!run) return []
  if (run.dateOnly) {
    return [
      ...(run.candidates
        ? [{ label: 'Candidates', text: run.candidates }]
        : []),
      {
        label: 'Run',
        text: `${run.date}, ${run.time}; ${
          run.candidates ? 'queries' : 'queries and candidates'
        } not recorded in the folder name`,
      },
    ]
  }
  const book = run.queryBook || queryBookTitle || 'the query book'
  let queries
  if (run.querySource === 'hand-picked') {
    queries = `the hand-picked ${book} glyphs (from workbench groupings) on ${pagesText(
      run
    )}`
  } else if (run.querySource === 'auto') {
    queries = `for each letter, the ${percent(
      run.q
    )} of glyphs from ${book} (${pagesText(
      run
    )}) that the damage detector scored most damaged (at least 200 per letter)`
  } else if (run.querySource === 'targeted') {
    queries = `every glyph on the ${book} pages that already have accepted matches`
  } else {
    queries = `${run.querySource} queries from ${book}, ${pagesText(run)}`
  }
  const candidates = `for each letter, the ${percent(run.c)} of glyphs from ${
    run.candidates
  } that the damage detector scored most damaged (at least 50 per candidate book)`
  return [
    { label: 'Queries', text: queries },
    {
      label: 'Candidates',
      text:
        parseFloat(run.c) >= 1 ? `all glyphs in ${run.candidates}` : candidates,
    },
    { label: 'Run', text: `${run.date}, ${run.time}` },
  ]
}

// "A_uc - (63390) A treatise partly theological,... p. 448-s l. 15 c. 37" -> "(63390) A treatise partly theological · p.448 l.15 c.37"
export function shortCharacterLabel(label) {
  if (!label) return ''
  const m = /^\w+ - (.*?)(?:,?\.\.\.)? p\. (\d+)-\w+ l\. (\d+) c\. (\d+)$/.exec(
    label
  )
  if (!m) return label
  return `${m[1]} · p.${m[2]} l.${m[3]} c.${m[4]}`
}

// Book folder + page from a character's IIIF image URL, e.g.
// .../books/redo/tbraddyll_R23639_mdp_8_religionandreasonREDO1688/pages_color/...-0342.tif/... -> "Religion and Reason (R23639) · p.342"
// (folders are <printer>_<ESTC>_<library>_<format>_<titleslug>[REDO]<year>; line/char are not in the URL)
function captionFromImage(image) {
  const url = image && (image.web_url || image.thumbnail || image.buffer)
  if (!url) return ''
  const m =
    /\/books\/[^/]+\/([^/]+)\/pages[^/]*\/[^/]*?-(\d{3,4})(?:_page\w*)?\.tif/.exec(
      url
    )
  if (!m) return ''
  const parts = m[1].split('_')
  const estc = parts.find((p) => /^[RT]\d+$/.test(p))
  const slug = (parts[4] || parts[parts.length - 1])
    .replace(/REDO|FAIL/g, '')
    .replace(/\d{4}$/, '')
  return `${bookName(slug)}${estc ? ` (${estc})` : ''} · p.${parseInt(m[2])}`
}

// Caption for a character: its database label when it has one, otherwise book and page from its image URL.
export function characterCaption(character) {
  if (!character) return ''
  return (
    shortCharacterLabel(character.label) || captionFromImage(character.image)
  )
}
