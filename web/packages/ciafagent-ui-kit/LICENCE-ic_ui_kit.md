ISC LICENSE
ISC_License_for_CIANCHOSAINT_ic_ui_kit (CIANCHOSAINT edition)
==============================================================

This file documents the LICENCE attribution for the wholesale-copied
ic-ui-kit files under web/packages/ciafagent-ui-kit/src/ic-web-components/
and web/packages/ciafagent-ui-kit/src/ic-react/.

The ic-ui-kit is dual-licensed under the Open Government Licence v3.0
(OGL-3.0) + the MIT licence.

1) MIT LICENCE (upstream — preserved wholesale)
----------------------------------------------

MIT License

Copyright (c) 2022 The Secret Intelligence Service (MI6)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

2) OPEN GOVERNMENT LICENCE v3.0 (upstream — preserved wholesale)
---------------------------------------------------------------

The ic-ui-kit (per its npm package name `@ukic/web-components` and
`@ukic/react`) is also released under the Open Government Licence v3.0
(OGL-3.0). The OGL-3.0 applies to the upstream Crown Copyright
attribution + the per-component CSS theming + the per-component icons.

Full licence text:
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

3) CIANCHOSAINT WRAPPER LICENCE (the integration wrappers)
----------------------------------------------------------

The 9 cianchosaint integration wrappers at
web/packages/ciafagent-ui-kit/src/ic-<component>.tsx are released under
the Business Source Licence v1.1 — CIANCHOSAINT edition (BUSL-1.1 v2) per
the root LICENSE.md.

4) WHAT THIS MEANS IN PRACTICE
------------------------------

- The wholesale-copied upstream files retain their original MIT + OGL-3.0
  licences. Per the OGL-3.0 §4(j), the upstream attribution is preserved
  at the top of every wholesale-copied .tsx / .ts file.
- Any MODIFICATIONS to the upstream files (e.g. namespace rename from
  `@ukic/` to `@cianchosaint/ciafagent-ui-kit/`) are released under the
  CIANCHOSAINT BUSL-1.1 v2 licence.
- The 9 integration wrappers (the new code) are BUSL-1.1 v2 — British-Isles
  public-sector bodies only.
- Every file in the wholesale-copy carries the licence attribution header
  added by scripts/add_wholesale_copy_headers.py — verifiable via
  `mise run cianchosaint:ic-ui-kit:smoke`.

5) UPSTREAM ATTRIBUTION
-----------------------

The upstream ic-ui-kit source is at:
  https://github.com/mi6/ic-ui-kit

The vendor (the Secret Intelligence Service, MI6) is responsible for the
upstream licence compliance. Cianchosaint preserves the MIT + OGL-3.0
attribution + the Crown Copyright attribution in each modified file.

End of LICENCE-ic_ui_kit attribution.
