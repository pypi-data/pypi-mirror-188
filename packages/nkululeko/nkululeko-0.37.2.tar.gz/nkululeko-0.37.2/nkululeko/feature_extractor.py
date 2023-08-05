# feature_extractor.py
import pandas as pd
from nkululeko.util import Util 
from nkululeko.feats_opensmile import Opensmileset


class FeatureExtractor:
    df = None # pandas dataframe to store the features (and indexed with the data from the sets)
    data_df = None # dataframe to get audio paths


    def __init__(self, data_df, data_name, feats_designation):
        self.data_df = data_df
        self.data_name = data_name
        self.util = Util()
        self.feats_designation = feats_designation

    def extract(self):
        strategy = self.util.config_val('DATA', 'strategy', 'traintest')
        feats_types = self.util.config_val_list('FEATS', 'type', ['os'])
        featExtractor = None
        self.feats= pd.DataFrame()
        _scale = True
        for feats_type in feats_types:
            store_name = f'{self.data_name}_{strategy}_{feats_type}'   
            if feats_type=='os':
                featExtractor = Opensmileset(f'{store_name}_{self.feats_designation}', self.data_df)
            elif feats_type=='trill':
                from nkululeko.feats_trill import TRILLset
                featExtractor = TRILLset(f'{store_name}_{self.feats_designation}', self.data_df)
            elif feats_type=='wav2vec':
                from nkululeko.feats_wav2vec2 import Wav2vec2
                featExtractor = Wav2vec2(f'{store_name}_{self.feats_designation}', self.data_df)
            elif feats_type=='audmodel':
                from nkululeko.feats_audmodel import AudModelSet
                featExtractor = AudModelSet(f'{store_name}_{self.feats_designation}', self.data_df)
            elif feats_type=='praat':
                from nkululeko.feats_praat import Praatset
                featExtractor = Praatset(f'{store_name}_{self.feats_designation}', self.data_df)
            elif feats_type=='mld':
                from nkululeko.feats_mld import MLD_set
                featExtractor = MLD_set(f'{store_name}_{self.feats_designation}', self.data_df)
            elif feats_type=='import':
                from nkululeko.feats_import import Importset
                featExtractor = Importset(f'{store_name}_{self.feats_designation}', self.data_df)
            else:
                self.util.error(f'unknown feats_type: {feats_type}')

            featExtractor.extract()
            featExtractor.filter()
            # remove samples that were not extracted by MLD
            #self.df_test = self.df_test.loc[self.df_test.index.intersection(featExtractor_test.df.index)]
            #self.df_train = self.df_train.loc[self.df_train.index.intersection(featExtractor_train.df.index)]
            self.util.debug(f'{feats_type}: shape : {featExtractor.df.shape}')
            self.feats = pd.concat([self.feats, featExtractor.df], axis = 1)
        return self.feats