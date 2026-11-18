# Independent verification, November 16 06:24 UTC

- GitHub run43803119616 fetched independently: full head9769d922cc8f3e908c0d611dd2f48df6418089cd, terminal failure. Debug job133087698819 failed, four other jobs passed.
- Artifact14198828420 independently fetched: app-tests-Debug,724246160bytes, unexpired, API digest `sha256:2b90932b5229614dd75fa682b708178f6ccdada4995f02dc4c3fdf449ff50675`. This is GitHub's artifact metadata, not a newly computed checksum of a locally retained ZIP.
- Re-exported act4 independently from the downloaded xcresult using its payloadRef and byte-compared it with the packet. Both SHA256 `5e475fe8611bdceb7ee493a22219d2c8d1724cb887d49c72bb2b923d294cc73c`.
- Seven trace-reader regression tests passed. The control act0 strict command returned0. The actual failed act4 strict command returned1 with missing frame15. This red evidence remains intentional and unmodified.
- The actual failed configuration is zoom1.25, tracking=true, Reduced Motion=false. Post-action gaps64.4489ms and315.5293ms bracket two missing-pose opportunities. There are63retained records. Update-entry gap316.7905ms minus prior measured update17.4317ms leaves299.3588ms unattributed. These are observations, not proof of host-only or production-only origin.
- Separately, full3ad31adfb956be6389bfc263c0515b89c51b7f9c is an ancestor of current runtime HEAD. Fourteen existing #238 portable native-evidence regressions passed independently in35.444s, including clamped-control and missing-loop rejection. This does not repair #237.

No original test assertion, production code, selector timing, gameplay, art, pin or issue lifecycle changed. The diagnostic regression is suitable for CI because it asserts that the historical failure stays visible, not that the failing runtime is fixed. Root cause remains unproven. No live native rerun or complete SpriteKit reproduction is claimed. Both defects remain open.
