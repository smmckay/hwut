
//#include "tn_cf_fsm.h"
#include "tn_dab_dispatch.h"
#include "tn_dab_db_ensemble.h"
#include "tn_dab_prot_cfg.h"


/* <<functions>> */
tn_cf_msg_class_t*            tnCfMsgCtor                   (tn_cf_msg_id_t             id,
                                                             tn_cf_active_obj_id_t      sender,
                                                             tn_cf_active_obj_id_t      receiver);


unsigned8   tnDabDbEnsembleGetDreId			      (tn_dab_db_ensemble_class_t* me);
tn_dab_db_ensemble_codec_t	tnDabDbEnsembleGetCurrAudioCodec      (tn_dab_db_ensemble_class_t* me);
unsigned8	tnDabDbEnsembleGetCurrAudioQuality	  (tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleIsAudioPlaying          (tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleIsDabPlaying            (tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleIsFmLinked              (tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleGetTreeVersion          (tn_dab_db_ensemble_class_t* me);
unsigned16  tnDabDbEnsembleGetEnsId			      (tn_dab_db_ensemble_class_t* me);
unsigned32  tnDabDbEnsembleGetServSIDByIdx          (tn_dab_db_ensemble_class_t* me, unsigned8                   serv_index);
unsigned8	tnDabDbEnsembleGetDABLinksBySID		    (tn_dab_db_ensemble_class_t*        me, tn_dab_db_serv_follow_dab_link_t*	link_list, unsigned8							list_size, unsigned32							sid, tn_dab_link_type_t					link_type);
unsigned8	tnDabDbEnsembleGetFMRDSLinksBySID		(tn_dab_db_ensemble_class_t*        me, tn_dab_db_serv_follow_fm_link_t*	link_list, unsigned8							list_size, unsigned32							sid, tn_dab_link_type_t					link_type);
void		tnDabDbEnsembleGetLabel			      (tn_dab_db_ensemble_class_t* me, tn_dab_label_t* label);
unsigned8   tnDabDbEnsembleGetEnsECC		      (tn_dab_db_ensemble_class_t* me);
unsigned16  tnDabDbEnsembleGetCompCIDByIdx			(tn_dab_db_ensemble_class_t* me, unsigned8 comp_index);
void        tnDabDbEnsembleGetCompLabelByIdx        (tn_dab_db_ensemble_class_t*        me, unsigned8                          serv_index, unsigned8                          comp_index, tn_dab_label_t*                    label);
unsigned8   tnDabDbEnsembleGetEnsValid             (tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleGetServCount     (tn_dab_db_ensemble_class_t*	me);
unsigned8	tnDabDbEnsembleGetServiceCompStartIdx	(tn_dab_db_ensemble_class_t* me, unsigned8                   serv_index);
unsigned8	tnDabDbEnsembleIsAudioService			(tn_dab_db_ensemble_class_t* me, unsigned8                   serv_index);
unsigned8	tnDabDbEnsembleIsAudioComponent			(tn_dab_db_ensemble_class_t*        me, unsigned8                          comp_index);
unsigned8 	tnDabDbEnsembleGetCurrServIdx 			(tn_dab_db_ensemble_class_t* me);
unsigned8 	tnDabDbEnsembleGetServIdxBySID 			(tn_dab_db_ensemble_class_t* me, unsigned32                  sid);
unsigned8 	tnDabDbEnsembleGetServIdxByShortSID     (tn_dab_db_ensemble_class_t* me, unsigned32                  sid);
void        tnDabDbEnsembleGetServInfo              (tn_dab_db_ensemble_class_t*        me, unsigned8                          serv_index, tn_dab_db_ensemble_serv_info_t*    serv_info);
unsigned8	tnDabDbEnsembleGetServiceCompCount		(tn_dab_db_ensemble_class_t* me, unsigned8                   serv_index);
tn_dab_db_ensemble_anncmnt_t tnDabDbEnsembleGetCurrAnncmntProperties (tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleGetAnncmntClusterFilterStatus(tn_dab_db_ensemble_class_t* me);
unsigned8   tnDabDbEnsembleGetAnncmntTypeFilterStatus   (tn_dab_db_ensemble_class_t* me);
void 		tnDabDbEnsembleSetAnncmnts (tn_dab_db_ensemble_class_t* me, tn_dab_db_ensemble_anncmnt_t* filtered_anncmnts);

unsigned8               tnDabProtCfgGetMuteThreshold            (tn_dab_db_ensemble_codec_t codec);
unsigned8               tnDabProtCfgGetUnmuteThreshold          (tn_dab_db_ensemble_codec_t codec);
unsigned8               tnDabProtCfgGetPreemptiveThreshold      (tn_dab_db_ensemble_codec_t codec);
unsigned8               tnDabProtCfgGetPreemptiveRequirement    (tn_dab_db_ensemble_codec_t codec);

unsigned32      tnCfStreamReadU32   (tn_cf_stream_class_t* me);
unsigned16      tnCfStreamReadU16   (tn_cf_stream_class_t* me);
unsigned8       tnCfStreamReadU8    (tn_cf_stream_class_t* me);
void            tnCfStreamReadStr   (tn_cf_stream_class_t* me, void* result, unsigned8 length);
void            tnCfStreamWriteU32  (tn_cf_stream_class_t* me, unsigned32 arg);
void            tnCfStreamWriteU16  (tn_cf_stream_class_t* me, unsigned16 arg);
void            tnCfStreamWriteU8   (tn_cf_stream_class_t* me, unsigned8 arg);
void            tnCfStreamWriteStr  (tn_cf_stream_class_t* me, const void* arg, unsigned8 length);

void                    tnCfTimerStartTimer     (tn_cf_msg_id_t           id,
                                                 tn_cf_active_obj_id_t    receiver,
                                                 unsigned32               time);

void                    tnCfTimerStopTimer      (tn_cf_msg_id_t id, tn_cf_active_obj_id_t    receiver);

unsigned8               tnCfTimerIsRunning      (tn_cf_msg_id_t id, tn_cf_active_obj_id_t receiver);


void            tnCfSchedSendMsg            (tn_cf_msg_class_t* msg);


unsigned8   tnDabFreqConvertFreqToDreId         (unsigned32 freq, unsigned8* dre_id);

void tnCfDbgDabStreamLearnList(tn_dab_learnmem_class_t*  me);
void tnCfDbgDabStreamLearnListEnsembleIdAtDreId(unsigned8 DreId, unsigned16 EnsId, unsigned8 EnsCC);










