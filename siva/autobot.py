from os import listdir
from os.path import isfile, join
import xlsxwriter
import pandas as pd
import re
import numpy as np
import warnings


class AutoBot:
    def __init__(self, file_path=r'/home/rmr327/Desktop/Z/CIP/',
                 output_file_name='output.xlsx'):
        self.file_path = file_path
        self.files = [f for f in listdir(file_path) if isfile(join(file_path, f)) and 'CSV' in f]
        self.files.sort()
        self.component_vals = {}
        self.output_excel = xlsxwriter.Workbook(file_path + output_file_name)
        self.worksheet = self.output_excel.add_worksheet()
        self.row = 14
        self.col = 0
        self.stats_index = ['Readings', 'Average', 'Std. Dev.', 'Max.', 'Min.', '90%', '95%']
        self.stats_df = pd.DataFrame(index=self.stats_index)

    def parse(self):
        for file in self.files:
            file_lower = file.lower()
            # comp files
            flag = True
            if 'lock' not in file_lower:
                df = pd.read_csv(self.file_path + file)
                vals = df.iloc[:, 1].values
                num_vals = len(vals)

                # If number of rows is more than 20 we will split the rows
                if 'gir' in file_lower:
                    flag = False
                    vals = np.split(vals, num_vals / 3)
                    key = re.sub(r".CSV", "", file)

                elif num_vals > 20:
                    if 'col' in file_lower:
                        print(file_lower)
                        vals = np.split(vals, num_vals / (num_vals/4))
                        key = re.sub(r".CSV", "", file)

                    elif ' ' in file:
                        vals = np.split(vals, num_vals / 20)
                        key = re.sub(r".CSV", "", file)

                    else:
                        vals = np.split(vals, num_vals/20)
                        key = re.sub(r"[0-9].CSV", "", file)
                    flag = False

                else:
                    if 'col' in file_lower:
                        vals = np.split(vals, num_vals / (num_vals/4))
                        key = re.sub(r".CSV", "", file)
                        flag = False
                    else:
                        key = re.sub(r"[0-9].CSV", "", file)

                if key in self.component_vals:
                    self.component_vals[key].append(vals)
                else:
                    if flag:
                        self.component_vals[key] = [vals]
                    else:
                        self.component_vals[key] = vals

    def action(self):
        # names_len = len(self.component_vals)
        tables = list(self.component_vals.keys())
        tables.sort()
        cell_format_1 = None
        cell_format_2 = None
        cell_format_val = None
        for i,  comp in enumerate(tables):
            cell_format_val = self.output_excel.add_format({'border': True, 'center_across': True})
            start_row = self.row
            start_col = self.col
            self.row = self.row + 2
            row_info = []
            deck_data = []
            row_count = 0

            for row_info in self.component_vals[comp]:
                self.worksheet.write_row(self.row, self.col, row_info, cell_format=cell_format_val)
                self.row += 1
                row_count += 1
                deck_data.extend(row_info)

            num_readings = len(deck_data)
            avg = np.round(np.mean(deck_data), 2)
            std = np.round(np.std(deck_data), 2)
            maximum = np.round(np.max(deck_data), 2)
            minimum = np.round(np.min(deck_data), 2)
            ninety_percent = np.round(avg - 1.282 * std, 2)
            ninety_5_percent = np.round(avg - 1.645 * std, 2)

            self.stats_df[comp] = [num_readings, avg, std, maximum, minimum, ninety_percent, ninety_5_percent]

            len_row_info = len(row_info)

            cell_format_1 = self.output_excel.add_format({'bold': True, 'font_color': 'white', 'center_across': True,
                                                          'border': True, 'bg_color': '#08085B'})
            cell_format_2 = self.output_excel.add_format({'bold': True, 'font_color': 'black', 'center_across': True,
                                                          'border': True, 'bg_color': '#E3E3E3', 'shrink': True})

            self.worksheet.merge_range(start_row, start_col, start_row, self.col + len_row_info-1,
                                       'Cover Data (inches)', cell_format=cell_format_1)
            self.worksheet.merge_range(start_row + 1, start_col, start_row + 1, self.col + len_row_info-1,
                                       comp, cell_format=cell_format_2)

            # next_deck = (i+1) % names_len
            # if new_col > 2*len_row_info + 1 or comp[0] != tables[next_deck][0]:
            #     self.col = 0
            #     self.row += 2
            # else:
            #     self.col = new_col
            #     self.row -= row_count + 2

            self.row += 2

        stats_cols = self.stats_df.columns
        # len_stats_cols = len(stats_cols)

        self.stats_df['Average'] = self.stats_df.mean(axis=1).round(2)

        i = 0
        for i, col in enumerate(stats_cols):
            self.worksheet.write_string(1, i + 1, col, cell_format=cell_format_2)
            self.worksheet.write_column(2, i+1, self.stats_df[col].values, cell_format=cell_format_val)

        self.worksheet.write_string(1, i + 2, 'All', cell_format=cell_format_2)
        self.worksheet.write_column(2, i + 2, self.stats_df['Average'].values, cell_format=cell_format_val)
        self.worksheet.write_column(2, 0, list(self.stats_index), cell_format=cell_format_val)

        self.worksheet.merge_range(0, 0, 0, i+2, 'Cover Statistics (inches)', cell_format=cell_format_1)

        # Total readings
        self.worksheet.write_number(2, i + 2, sum(self.stats_df.loc['Readings', :].values[:-1]),
                                    cell_format=cell_format_val)

        self.output_excel.close()


if __name__ == '__main__':
    warnings.simplefilter(action='ignore', category=FutureWarning)
    bot = AutoBot()
    bot.parse()
    bot.action()
