import traceback
from abc import ABC, abstractmethod
from typing import Optional
from pprint import pformat

from tabulate import tabulate

from dipdup import spec_version_mapping

_migration_required_message = """Project migration required!

{version_table}

  1. Run `dipdup migrate`
  2. Review and commit changes

See https://baking-bad.org/blog/ for additional release information.
"""

_handler_import_message = """Failed to import `{obj}` from `{module}`.

Reasons in order of possibility:

  1. `init` command was not called after modifying config
  2. Name of handler module and handler function inside it don't match
  2. Invalid `package` config value, reusing name of existing package
  3. Something's wrong with PYTHONPATH env variable

"""

_contract_already_exists_error = """Contract with name `{name}` or address `{address}` already exists.

Active contracts:
{contracts_table}
"""

_index_already_exists_error = """Index with name `{name}` already exists.

Active indexes:
{indexes_table}
"""

_data_validation_error = """Failed to validate operation/big_map data against a generated type class.

Invalid data:
{invalid_data}
"""

_tab = '\n\n' + ('_' * 80) + '\n\n'


class DipDupError(ABC, Exception):
    exit_code = 1

    def __init__(self, ctx) -> None:
        super().__init__()
        self.ctx = ctx

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.__doc__}'

    @abstractmethod
    def format_help(self) -> str:
        ...

    def format(self) -> str:
        exc = f'\n\n{traceback.format_exc()}'.rstrip()
        return _tab.join([exc, self.format_help() + '\n'])


class ConfigurationError(DipDupError):
    """DipDup YAML config is invalid"""

    def __init__(self, msg: str) -> None:
        super().__init__(None)
        self.msg = msg

    def format_help(self) -> str:
        return f"{self.msg}\n\nDipDup config reference: https://docs.dipdup.net/config-file-reference\n"


class MigrationRequiredError(DipDupError):
    """Project and DipDup spec versions don't match """

    def __init__(self, ctx, from_: str, to: str) -> None:
        super().__init__(ctx)
        self.from_ = from_
        self.to = to

    def format_help(self) -> str:
        version_table = tabulate(
            [
                ['current', self.from_, spec_version_mapping[self.from_]],
                ['required', self.to, spec_version_mapping[self.to]],
            ],
            headers=['', 'spec_version', 'DipDup version'],
        )
        return _migration_required_message.format(version_table=version_table)


class HandlerImportError(DipDupError):
    """Can't perform import from handler module"""

    def __init__(self, module: str, obj: Optional[str] = None) -> None:
        super().__init__(None)
        self.module = module
        self.obj = obj

    def format_help(self) -> str:
        return _handler_import_message.format(obj=self.obj or '', module=self.module)


class ContractAlreadyExistsError(DipDupError):
    """Attemp to add a contract with alias or address which is already in use"""

    def __init__(self, ctx, name: str, address: str) -> None:
        super().__init__(ctx)
        self.name = name
        self.address = address

    def format_help(self) -> str:
        contracts_table = tabulate([(name, c.address) for name, c in self.ctx.config.contracts.items()])
        return _contract_already_exists_error.format(name=self.name, address=self.address, contracts_table=contracts_table)


class IndexAlreadyExistsError(DipDupError):
    """Attemp to add an index with alias which is already in use"""

    def __init__(self, ctx, name: str) -> None:
        super().__init__(ctx)
        self.name = name

    def format_help(self) -> str:
        indexes_table = tabulate([(name,) for name in self.ctx.config.indexes.values()])
        return _index_already_exists_error.format(name=self.name, indexes_table=indexes_table)


class InvalidDataError(DipDupError):
    """Failed to validate operation/big_map data against a generated type class"""

    def __init__(self, ctx, data) -> None:
        super().__init__()
        self.data = data

    def format(self) -> str:
        return _data_validation_error.format(invalid_data=self.data)
