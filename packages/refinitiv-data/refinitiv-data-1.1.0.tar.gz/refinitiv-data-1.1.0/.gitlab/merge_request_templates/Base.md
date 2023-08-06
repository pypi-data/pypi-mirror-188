## Check list when creating MR:

- [ ] **Ticket number** in title (if has)


## Check list before merging MR:

- [ ] Run unit **tests**
- [ ] Refactor unit **tests** (if failing when code changed)
- [ ] Add unit **tests** (if new class/method was added)
- [ ] Remove **WIP status** if the MR is ready for review
- [ ] Move [Jira **ticket**](https://jira.refinitiv.com/secure/Dashboard.jspa) into _"Code Review"_
- [ ] Update [**Confluence page**](https://confluence.refinitiv.com/display/EF/2.+RD+Lib+Python+-+Technical+Requirements) (if requirements were added or changed)
- [ ] Add **docstrings** to public methods/classes (if needed)
- [ ] Add **typing annotations** to public classes/methods (if needed)
- [ ] **DO NOT MERGE** without approve from QA

## Check list while merging MR:

- [ ] At least **2 kudos** from devs[^2] and at least one from QA[^2]
- [ ] Check _**Delete source branch** and _**Squash commits** when merge request is accepted._


### Notes:

Please try to keep _1 task = 1 branch, and use _git --rebase_.

Do not forget to add **EAPI-XXXX** to your commit name.

[Guideline](https://chris.beams.io/posts/git-commit/) about commit messages.

Use `black` for code formatting.
[Code style`s tools setup](https://teams.microsoft.com/l/entity/com.microsoft.teamspace.tab.wiki/tab::986a300e-df08-48d6-8e64-68470009a68a?context=%7B%22subEntityId%22%3A%22%7B%5C%22pageId%5C%22%3A41%2C%5C%22origin%5C%22%3A2%7D%22%2C%22channelId%22%3A%2219%3A7b9be5a7c5a74338b02f8e7e8adc5911%40thread.tacv2%22%7D&tenantId=71ad2f62-61e2-44fc-9e85-86c2827f6de9)

### For run unit tests:

Dependencies:

    pytest
    pytest-asyncio
    pytest-md
    asyncmock
    pytest-tornasync

Command:

    (.venv) ./refinitiv-data/dataplatform_project> python -m pytest ./tests/unit --md ./tests/{yoursurname}-report.md
    (.venv) ./refinitiv-data/dataplatform_project> python -m coverage run -m pytest ./tests/unit --md ../{yoursurname}-report.md
    (.venv) ./refinitiv-data/dataplatform_project> coverage report -m
    (.venv) ./refinitiv-data/dataplatform_project> coverage html

[^2]: Devs: Pierre.FAUREL, Artem.Kharchyshyn, Roman.Myronenko_rft, Taras.Konchak_rft, Andrii.Yatsyniak_rft, Alexandr.Andreyev_rft, Yurii.Shnitkovskyi_rft, Oleksii.Zhytnyk_rft. QAs: Roman.Mhoian_rft, Andrii.Sidachenko_rft

✌️