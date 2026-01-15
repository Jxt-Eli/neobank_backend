# neobank-backend

Minimal FastAPI backend for a neobank-style service — user auth, balances, transfers, transaction history and a small currency-conversion helper.

## Features
- FastAPI async endpoints
- JWT-based authentication (HTTP Bearer)
- Async SQLAlchemy session (AsyncSession)
- Basic endpoints: login, get balance, create transfer, list transactions, create user, currency conversion helper

## Prerequisites
- Python 3.11+ (tested)
- PostgreSQL (recommended) or other DB supported by SQLAlchemy async drivers
- Linux environment (development commands below use bash)

## Quick start

1. Clone and enter project
```bash
git clone <repo-url> && cd neobank-backend
```

2. Create virtualenv and install
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
# if a requirements.txt exists:
pip install -r requirements.txt
# otherwise (typical dependencies)
pip install fastapi uvicorn httpx sqlalchemy asyncpg pydantic python-jose[cryptography]
```

3. Environment
Create a `.env` file at project root (dotenv format). Example:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
SECRET_KEY=supersecretkey
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
Adjust keys to match your config.

4. Run the app (development)
```bash
./launch.sh
```
Open http://127.0.0.1:8000/docs for interactive API docs.

## Typical endpoints (examples)
- GET /                 — service root / status
- GET /health           — health check
- POST /login           — returns JWT (email/password)
- GET /balance          — requires Bearer token, returns user balance
- POST /transfer        — create a transfer (authenticated)
- GET /transactions     — list transactions (authenticated), supports limit/offset
- POST /users           — create new user
- GET /convert/{amount} — currency conversion helper

Refer to /docs for exact request/response schemas and models.

## Authentication
- Endpoints that require authentication use HTTP Bearer JWT tokens.
- Example usage:
```bash
# get token
curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"pass"}'

# using token
curl -H "Authorization: Bearer <TOKEN>" "http://127.0.0.1:8000/balance"
```

## Database & migrations
- The code uses SQLAlchemy AsyncSession. If you use PostgreSQL, install `asyncpg`.
- If you add migrations, use Alembic configured for async SQLAlchemy (recommended).

## Tests
- Add tests under `tests/` and run:
```bash
pytest
```

## Contributing
- Open issues or PRs. Keep changes small and include tests where applicable.

## License
GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

Copyright (C) 2025 Jxt-Eli
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

Preamble

The GNU General Public License is a free, copyleft license for
software and other kinds of works.

[Full GPLv3 text follows. The text below is the complete license.]

Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

0. Definitions.

   "This License" refers to version 3 of the GNU General Public License.

   "Copyright" also means copyright-like laws that apply to other kinds of
   works, such as semiconductor masks.

   "The Program" refers to any copyrightable work licensed under this
   License.  Each licensee is addressed as "you".  "Licensees" and
   "recipients" may be individuals or organizations.

   To "modify" a work means to copy from or adapt all or part of the work
   in a fashion requiring copyright permission, other than the making of an
   exact copy.  The resulting work is called a "modified version" of the
   earlier work or a work "based on" the earlier work.

   A "covered work" means either the unmodified Program or a work based
   on the Program.

   To "propagate" a work means to do anything with it that, without
   permission, would make you directly or secondarily liable for
   infringement under applicable copyright law, except executing it on a
   computer or modifying a private copy.  Propagation includes copying,
   distribution (with or without modification), making available to the
   public, and in some countries other activities as well.

   To "convey" a work means any kind of propagation that enables other
   parties to make or receive copies.  Mere interaction with a user through
   a computer network, with no transfer of a copy, is not conveying.

1. Source Code.

   The "source code" for a work means the preferred form of the work for
   making modifications to it.  "Object code" means any non-source form of
   a work.

   A "Standard Interface" means an interface that either is an official
   standard defined by a recognized standards body, or, in the case of
   interfaces specified for a particular programming language, one that
   is widely used among developers working in that language.

   The "System Libraries" of an executable work include anything, other
   than the work as a whole, that (a) is included in the normal form of
   packaging a Major Component, but which is not part of that Major
   Component, and (b) serves only to enable use of the work with that
   Major Component, or to implement a Standard Interface for which an
   implementation is available to the public in source code form.  A
   "Major Component", in this context, means a major essential component
   (kernel, window system, and so on) of the specific operating system
   (if any) on which the executable work runs, or a compiler used to
   produce the work, or an object code interpreter used to run it.

2. Basic Permissions.

   All rights granted under this License are granted for the term of
   copyright on the Program, and are irrevocable provided the stated
   conditions are met.  This License explicitly affirms your unlimited
   permission to run the unmodified Program.  The output from running a
   covered work is covered by this License only if the output, given its
   content, constitutes a covered work.  This License acknowledges your
   rights of fair use or other equivalent, as provided by copyright law.

   You may make, run and propagate covered works that you do not convey,
   without conditions so long as your license otherwise remains in force.
   You may convey covered works to others for the sole purpose of having
   them make modifications exclusively for you, or provide you with
   facilities for running those works, provided that you comply with the
   terms of this License in conveying all material for which you do not
   control copyright.  Those thus making or running the covered works for
   you must do so exclusively on your behalf, under your direction and
   control, on terms that prohibit them from conveying the works outside
   your control.

   Conveying under any other circumstances is permitted solely under the
   conditions stated below.  Sublicensing is not allowed; section 10 makes
   it unnecessary.

3. Protecting Users' Legal Rights From Anti-Circumvention Law.

   No covered work shall be deemed part of an effective technological
   measure under any applicable law fulfilling obligations under article
   11 of the WIPO copyright treaty adopted on 20 December 1996, or
   similar laws prohibiting or restricting circumvention of such
   measures.

   When you convey a covered work, you waive any legal power to forbid
   circumvention of technical measures to the extent such circumvention is
   effected by exercising rights under this License with respect to the
   covered work, and you disclaim any intention to limit operation or
   modification of the work as a means of enforcing, against the work's
   users, your or third parties' legal rights to forbid circumvention of
   technological measures.

4. Conveying Verbatim Copies.

   You may convey verbatim copies of the Program's source code as you
   receive it, in any medium, provided that you conspicuously and
   appropriately publish on each copy an appropriate copyright notice;
   keep intact all notices stating that this License and any
   non-permissive terms added in accord with section 7 apply to the code;
   keep intact all notices of the absence of any warranty; and give all
   recipients a copy of this License along with the Program.

   You may charge any price or no price for each copy that you convey,
   and you may offer support or warranty protection for a fee.

5. Conveying Modified Source Versions.

   You may convey a work based on the Program, or the modifications to
   produce it from the Program, in the form of source code under the
   terms of section 4, provided that you also meet all of these
   conditions:

     a) The work must carry prominent notices stating that you modified
     it, and giving a relevant date.

     b) The work must carry prominent notices stating that it is
     released under this License and any conditions added under section
     7.  This requirement modifies the requirement in section 4 to
     "keep intact all notices".

     c) You must license the entire work, as a whole, under this License
     to anyone who comes into possession of a copy.  This License
     therefore applies, along with any applicable section 7 additional
     terms, to the whole of the work, and all its parts, regardless of
     how they are packaged.  This License gives no permission to license
     the work in any other way, but it does not invalidate such
     permission if you have separately received it.

     d) If the work has interactive user interfaces, each must display
     Appropriate Legal Notices; however, if the Program has interactive
     interfaces that do not display Appropriate Legal Notices, your
     work need not make them do so.

6. Conveying Non-Source Forms.

   You may convey a covered work in object code form under the terms of
   sections 4 and 5, provided that you also convey the machine-readable
   Corresponding Source under the terms of this License, in one of the
   following ways:

     a) Convey the object code in, or embodied in, a physical product
     (including a physical distribution medium), accompanied by a
     conspicuous written offer, valid for at least three years and
     valid for as long as you offer spare parts or customer support for
     that product, to give anyone who possesses the object code either
     (1) a copy of the Corresponding Source for all the software in the
     product that is covered by this License, on a durable physical
     medium customarily used for software interchange, for a price no
     more than your reasonable cost of physically performing this
     conveying of source, or (2) access to copy the
     Corresponding Source from a network server at no charge.

     b) Accompany the object code with a copy of the Corresponding
     Source on a durable physical medium customarily used for software
     interchange.

     c) Convey individual copies of the object code with a copy of the
     written offer to provide the Corresponding Source.  This option is
     allowed only occasionally and noncommercially, and only if you
     received the object code with such an offer, in accord with
     subsection 6a.

     d) Convey the object code by offering access from a designated
     place (gratis or for a charge), and offer equivalent access to the
     Corresponding Source in the same way through the same place at no
     further charge.  You need not require recipients to copy the
     Corresponding Source along with the object code.

     e) Convey the object code using peer-to-peer transmission, provided
     you inform other peers where the object code and Corresponding
     Source of the work are being offered to the general public at no
     charge under subsection 6d.

   A separable portion of the object code, whose source code is omitted
   from the Corresponding Source because it is a System Library, need not
   be included in conveying the object code work.

7. Additional Terms.

   "Additional permissions" are terms that supplement the terms of this
   License by making exceptions from one or more of its conditions.
   Additional permissions that are applicable to the entire Program shall
   be treated as though they were included in this License, to the extent
   that they are valid under applicable law.  If additional permissions
   are granted only for parts of the library, those parts can be used
   separately under those permissions, but the entire library still
   remains covered by this License without regard to the additional
   permissions.

   When you convey a copy of a covered work, you may at your option
   remove any additional permissions from that copy, or from any part of
   it.  (Additional permissions may be written to require their own
   removal in certain cases when you modify the work.)

   You may add terms to a covered work in the following three cases:
     * The requirements of sections 4 and 5, combined with other
       conditions, apply to the entire covered work, and you may add a
       license that gives additional permissions to some or all parts of
       the covered work.
     * You may supplement the terms of this License with terms that
       regulate use of user interfaces for example require preservation
       of specified screens or legal notices, or prohibit misrepresenting
       the origin of the work.
     * You may add a patent license to a covered work.

   These additional terms must be listed in the source code and must not
   conflict with the rest of this License.

8. Termination.

   You may not propagate or modify a covered work except as expressly
   provided under this License.  Any attempt otherwise to propagate or
   modify it is void and will automatically terminate your rights under
   this License (including any patent licenses granted under the third
   paragraph of section 11).

   However, if you cease all violation of this License, then your
   license from a particular copyright holder is reinstated (a)
   provisionally, unless and until the copyright holder explicitly and
   finally terminates your license, and (b) permanently, if the copyright
   holder fails to notify you of the violation by some reasonable means
   prior to 60 days after the cessation.

9. Acceptance Not Required for Having Copies.

   You are not required to accept this License in order to receive or
   run a copy of the Program.  Ancillary propagation of a covered work
   occurring solely as a consequence of using peer-to-peer transmission
   to receive a copy likewise does not require acceptance.  However, no
   one can convey a covered work except under this License.  Therefore,
   programs distributed by parties who have not accepted this License
   are not subject to its requirements.

10. Automatic Licensing of Downstream Recipients.

   Each time you convey a covered work, the recipient automatically
   receives a license from the original licensors, to run, modify and
   propagate that work, subject to this License.  You are not responsible
   for enforcing compliance by third parties.

11. Patents.

   A "contributor" is a copyright holder who authorizes use under this
   License of the Program or a work on which the Program is based.  The
   work thus licensed is called the contributor's "contributions".

   Each contributor grants you a non-exclusive, worldwide, royalty-free
   patent license under the contributor's essential patent claims, to
   make, use, sell, offer for sale, import and otherwise run, modify and
   propagate the contents of its contribution.

   In the following three paragraphs, a patent license is a license
   acquired by a contributor, whether already acquired or hereafter
   acquired, and is not a defense to infringement claims outside its
   scope.

   If you convey a covered work, knowingly relying on a patent license,
   and you engage in patent litigation alleging that the Program (or a
   contribution) infringes a patent, then your rights under this License
   to propagate the work are terminated.

   If you convey a covered work, and a third party brings a patent claim
   against you alleging that the work as conveyed infringes a patent,
   the recipient has the right to ask the contributor to defend the
   recipient against that claim, and the contributor may be required to
   provide such a defense if the contributor has the ability to do so.

12. No Surrender of Others' Freedom.

   If conditions are imposed on you (whether by court order, agreement or
   otherwise) that contradict the conditions of this License, they do
   not excuse you from the conditions of this License.  If you cannot
   comply with both this License and other obligations, then you may not
   convey the work at all.  For example, if a patent license would not
   permit royalty-free redistribution of the Program by all those to whom
   the patent license applies, the only way you could comply with both it
   and this License would be to refrain entirely from distribution of the
   Program.

13. Use with the GNU Affero General Public License.

   Notwithstanding any other provision of this License, you have
   permission to link or combine any covered work with a work licensed
   under version 3 of the GNU Affero General Public License into a single
   combined work, and to convey the resulting work.  The terms of this
   License will continue to apply to the part which is the covered work,
   but the special requirements of the GNU Affero General Public License,
   section 13, concerning remote network interaction apply to the
   combination as provided in that section.

14. Revised Versions of this License.

   The Free Software Foundation may publish revised and/or new versions
   of the GNU General Public License from time to time.  Such new versions
   will be similar in spirit to the present version, but may differ in
   detail to address new problems or concerns.

   Each version is given a distinguishing version number.  If the
   Program specifies that a certain numbered version of the GNU General
   Public License "or any later version" applies to it, you have the
   option of following the terms and conditions either of that specified
   version or of any later version that has been published (not as a
   draft) by the Free Software Foundation.  If the Program does not
   specify a version number of this License, you may choose any version
   ever published by the Free Software Foundation.

15. Disclaimer of Warranty.

   THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
   APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
   HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT
   WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND
   PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE PROGRAM PROVE
   DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR
   CORRECTION.

16. Limitation of Liability.

   IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
   WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
   THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING
   ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT
   OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
   TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED
   BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY
   OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED
   OF THE POSSIBILITY OF SUCH DAMAGES.
