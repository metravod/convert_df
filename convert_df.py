import pandas as pd
from pandas import DataFrame
from typing import List, Dict, Tuple, Any, Union, Optional


class ConvertDF:

    def __init__(
            self,
            input_df: DataFrame,
            cols: List[str] = None,
            rename_cols: Union[str, Dict[str, str]] = None,
            type_cols: Union[type, Dict[str, type], None] = None,
            is_oneliner: bool = False
    ):
        self._input_df = input_df
        self._cols = cols
        self._rename_cols = rename_cols
        self._type_cols = type_cols
        self._is_oneliner: bool = is_oneliner
        self._empty_row = ()
        self._define_final_cols()

    def _is_df_oneliner(self) -> bool:
        return True if len(self._input_df) == 1 else False

    def _is_df_empty(self) -> bool:
        return True if len(self._input_df) == 0 else False

    def _get_range(self) -> range:
        return range(0, len(self._input_df))

    def _define_final_cols(self) -> None:
        """Финальные ключи с учетом переименования"""
        if self._cols and self._rename_cols:
            self._final_cols = {
                col: self._rename_cols[col]
                if col in self._rename_cols.keys() else col
                for col in self._cols
            }
        elif self._cols:
            self._final_cols = {col: col for col in self._cols}
        else:
            self._final_cols = {col: col for col in self._input_df.columns}
        self._cols = [col for col in self._final_cols.keys()]

    def _get_value(self, row: Tuple[Any], col: str) -> Any:
        """Забираем из нужного столбца значение и приводим к нужному типу"""
        type_value = self._define_type_col(self._type_cols, col)
        value = getattr(row, col) if pd.notna(getattr(row, col)) else None
        return type_value(value) if type_value and value else value

    @staticmethod
    def _define_type_col(type_cols: Union[type, Dict[str, type], None], col: str) -> Optional[type]:
        if isinstance(type_cols, type):
            return type_cols
        elif isinstance(type_cols, dict):
            return type_cols[col]
        else:
            return None

    def _define_final_result(self, result: list) -> Union[list, dict]:
        return result[0] if len(result) == 1 and self._is_oneliner else result

    def to_dict(self) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        return (
            {self._final_cols[col]: None for col in self._cols} if self._is_df_empty()
            else self._define_final_result([
                {self._final_cols[col]: self._get_value(row, col) for col in self._cols}
                for row in self._input_df[self._cols].itertuples(index=False)
            ])
        )

    def to_list(self) -> Union[List[Any], List[List[Any]], None]:
        return (
            [None for col in self._cols] if self._is_df_empty()
            else self._define_final_result([
                [self._get_value(row, col) for col in self._cols]
                for row in self._input_df[self._cols].itertuples(index=False)
            ])
        )
