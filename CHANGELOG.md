# Changelog

## 1.0.0 (2026-05-02)


### Features

* add `get analysis file prefix` action ([#23](https://github.com/gmc-norr/st2-cleve/issues/23)) ([2331ca4](https://github.com/gmc-norr/st2-cleve/commit/2331ca4bca6343411d62f278aafafff6350cf825))
* add `get_run_qc` action ([#27](https://github.com/gmc-norr/st2-cleve/issues/27)) ([bb903bd](https://github.com/gmc-norr/st2-cleve/commit/bb903bd4f8f995b8afadaf8e387e768250a1084b))
* add analysis action ([#17](https://github.com/gmc-norr/st2-cleve/issues/17)) ([9fcbbb5](https://github.com/gmc-norr/st2-cleve/commit/9fcbbb511486bdb14ac70f5fa0dac394a09be57a))
* add get analyses action ([#13](https://github.com/gmc-norr/st2-cleve/issues/13)) ([bcb9455](https://github.com/gmc-norr/st2-cleve/commit/bcb9455fe4e90d12218df823e36e934316af5cfb))
* add get samplesheet action ([#14](https://github.com/gmc-norr/st2-cleve/issues/14)) ([f9afa39](https://github.com/gmc-norr/st2-cleve/commit/f9afa392e8a11d70acbbbd904108d2df685bba3b))
* add get_analysis_files action ([#19](https://github.com/gmc-norr/st2-cleve/issues/19)) ([feae90c](https://github.com/gmc-norr/st2-cleve/commit/feae90cf8f2f556e089148e67be9df73f283371f))
* add Illumina directory sensor ([#6](https://github.com/gmc-norr/st2-cleve/issues/6)) ([800909c](https://github.com/gmc-norr/st2-cleve/commit/800909cc320ce40bb2a1427155337329087d56e3))
* add interop analysis file support ([#20](https://github.com/gmc-norr/st2-cleve/issues/20)) ([7046f4e](https://github.com/gmc-norr/st2-cleve/commit/7046f4e8cdd6e63f289572d76a850ef4bafb93e5))
* add run workflow ([#9](https://github.com/gmc-norr/st2-cleve/issues/9)) ([afc2155](https://github.com/gmc-norr/st2-cleve/commit/afc2155efeb17e345731507e0521edf4b8537d8e))
* add the new analysis file types to the get analysis files action ([#21](https://github.com/gmc-norr/st2-cleve/issues/21)) ([c3bd2e3](https://github.com/gmc-norr/st2-cleve/commit/c3bd2e3c4fbdd92fbb9daa675305c754e3306a52))
* add trigger for updated analysis state ([#11](https://github.com/gmc-norr/st2-cleve/issues/11)) ([2f0c72b](https://github.com/gmc-norr/st2-cleve/commit/2f0c72b31df11d85f1f6bea34fddfc4a965c570a))
* add trigger for updated run state ([#10](https://github.com/gmc-norr/st2-cleve/issues/10)) ([155e7a4](https://github.com/gmc-norr/st2-cleve/commit/155e7a40b11da9d0e3e30b71220c07f5a798efe1))
* add update analysis action ([#16](https://github.com/gmc-norr/st2-cleve/issues/16)) ([a514999](https://github.com/gmc-norr/st2-cleve/commit/a5149990153be021009c58de26178c838e32c85e))


### Bug Fixes

* address sensor issues ([#8](https://github.com/gmc-norr/st2-cleve/issues/8)) ([54e48cb](https://github.com/gmc-norr/st2-cleve/commit/54e48cbe19c9a454235a74ea1aee7fd983df4c12))
* change `add_analysis` file parameters to array of objects ([#25](https://github.com/gmc-norr/st2-cleve/issues/25)) ([b06dbff](https://github.com/gmc-norr/st2-cleve/commit/b06dbffbd3f6ef7b991561571c92077ab900668e))
* change `update analysis` parameter files to array of objects ([#24](https://github.com/gmc-norr/st2-cleve/issues/24)) ([c87884a](https://github.com/gmc-norr/st2-cleve/commit/c87884ab58a83278ce1e42e6c76fa387dd02ca23))
* make api_key parameter not required for update_run ([cba5684](https://github.com/gmc-norr/st2-cleve/commit/cba5684677118eaf9747e662c2af47359765443a))
* remove analysis id param from add analysis action ([#22](https://github.com/gmc-norr/st2-cleve/issues/22)) ([13641c5](https://github.com/gmc-norr/st2-cleve/commit/13641c5e613544e6325a5196a7ea77dbca3fac4e))
* remove unnecessary (or doubled) url encoding ([#26](https://github.com/gmc-norr/st2-cleve/issues/26)) ([9f2a00b](https://github.com/gmc-norr/st2-cleve/commit/9f2a00b98a30b4ae11e680eed40818b574241707))
* use verify param in request to avoid SSL errors ([#28](https://github.com/gmc-norr/st2-cleve/issues/28)) ([9e652b5](https://github.com/gmc-norr/st2-cleve/commit/9e652b51531dcfe207aa61cf28b7f688d87aeb91))
