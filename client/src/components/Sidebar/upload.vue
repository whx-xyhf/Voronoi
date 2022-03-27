<template>
  <div>
    <el-upload
      class="upload-demo"
      drag
      :on-change="upload"
      :file-list="file"
      :auto-upload="false"
      accpet="application/json"
      :show-file-list="false"
      action="/"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
      <div class="el-upload__tip" slot="tip">
          上传json
      </div>
    </el-upload>
  </div>
</template>

<script>
/* eslint-disable */
export default {
    
    data:()=>({
        file: [],
    }),

    methods: {
        upload(file, filelist) {
            const fileName = file.name
            this.$store.dispatch('updateFileName',fileName);
            const formData = new FormData();
            formData.append('file', file.raw);
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            this.$axios.post('upload_file', formData, config)
            .then(res=>{
                let data = JSON.parse(res.data.data)
                this.$store.dispatch('updateOriginData',data);
                this.sampling_rate = 100;
            })
        }
    },

    watch: {
        file() {
            console.log(this.file)
        }
    }

};
</script>

<style></style>
