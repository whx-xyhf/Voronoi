const actions={

    updateFileName({commit},names){
        commit('setFileName',names);
    },
    
    updateOriginData({commit},data){
        commit('setOriginData',data);
    },

    updateSamplingData({commit},data){
        commit('setSamplingData',data);
    },

    updateColorMap({commit},data){
        commit('setColorMap',data);
    },

    updateOpacity({commit},opacity){
        commit('setOpacity',opacity);
    },

    updateStrokeWidth({commit},width){
        commit('setStrokeWidth',width);
    },

    updateLayer({commit},layer){
        commit('setLayer',layer);
    },

    updateCurrentColorMapMethod({commit},method){
        commit('setCurrentColorMapMethod',method);
    },

    updateSampleState({commit},data){
        commit('setSampleState',data);
    }
};
export default actions;