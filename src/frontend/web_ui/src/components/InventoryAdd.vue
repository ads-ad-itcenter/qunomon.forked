<template>
<div>
    <modal name="inventoryAddModal" class="modalContents">
        <span class="subtitle">{{$t("inventoryAppend.mes")}}</span>
        <div class="error">
            <ui v-for="errorMessage in errorMessages" v-bind:key="errorMessage.text">
                <li class="error_message">{{ errorMessage }}</li>
            </ui>
        </div>
        <p id="asterisk"><span class="error">&#042;</span> {{$t("common.require")}}</p>
        <hr />
        <!--テキストボックス-->
        <div class="input">
            <form class="formCreate">
                <dl>
                    <dt class="label">{{$t("inventoryAppend.name")}}<span class="error">&#042;</span></dt>
                    <dd>
                        <template v-if="$i18n.locale === 'en'">
                            <input type="text" size="50" placeholder="Enter Inventory Name" name="project_name" v-model="name" />
                        </template>
                        <template v-else>
                            <input type="text" size="50" placeholder="インベントリ名を入力してください" name="project_name" v-model="name" />
                        </template>
                    </dd>
                </dl>
                <dl>
                    <dt class="label">{{$t("inventoryAppend.filePath")}}<span class="error">&#042;</span></dt>
                    <dd>
                        <input type="text" size="50" placeholder="C:\..." name="file_path" v-model="filePath"/>
                    </dd>
                </dl>
                <div class="formatError" v-if="isInvalidFormat">{{$t("inventoryAppend.formatError")}}</div>
                <dl>
                    <dt class="label">{{$t("inventoryAppend.dataType")}}<span class="error">&#042;</span></dt>
                    <dd>
                        <select class="select" v-model="selectedType" disabled>
                            <option value="" hidden style="color: gray">
                                {{$t("common.defaultPulldown")}}
                            </option>
                            <option v-for="dataType in dataTypes" :key="dataType.Id" v-bind:value="dataType.Id">
                                {{ dataType.Name }}
                            </option>
                        </select>
                    </dd>
                </dl>
                <dl>
                    <dt class="label">{{$t("inventoryAppend.fileSystem")}}<span class="error">&#042;</span></dt>
                    <dd>
                        <select class="select" v-model="selectedFileSystem">
                            <option value="" hidden style="color: gray">
                                {{$t("common.defaultPulldown")}}
                            </option>
                            <option v-for="fileSystem in fileSystems" :key="fileSystem.Id" v-bind:value="fileSystem.Id">
                                {{ fileSystem.Name }}
                            </option>
                        </select>
                    </dd>
                </dl>
                <dl>
                    <dt class="label">{{$t("inventoryAppend.format")}}<span class="error">&#042;</span></dt>
                    <dd>
                        <select class="select" v-model="selectedFormatType" disabled>
                            <option value="" hidden style="color: gray">
                                {{$t("common.defaultPulldown")}}
                            </option>
                            <!--inventory用にする-->
                            <option v-for="formatType of formatTypes" :key="formatType">
                                {{ formatType }}
                            </option>
                        </select>
                        <select class="select" v-model="selectedFormats" disabled>
                            <option value="" hidden style="color: gray">
                                {{$t("common.defaultPulldown")}}
                            </option>
                            <!--inventory用にする-->
                            <option v-for="format in formats" :key="format.Id">
                                {{ format.Format }}
                            </option>
                        </select>
                    </dd>
                </dl>
                <dl>
                    <dt class="label">{{$t("inventoryAppend.description")}}</dt>
                    <dd>
                        <textarea name="example" cols="50" rows="6" v-model="description"></textarea>
                    </dd>
                </dl>
                <div id="btn_set">
                    <template v-if="$i18n.locale === 'en'">
                        <input type="button" value="Cancel" class="btn_left" @click="postInventoryCancel" />
                        <input type="button" value="Create" class="btn_right" @click="postInventory" />
                    </template>
                    <template v-else>
                        <input type="button" value="キャンセル" class="btn_left" @click="postInventoryCancel" />
                        <input type="button" value="作成" class="btn_right" @click="postInventory" />
                    </template>
                </div>
            </form>
        </div>
        <div id="closeModal" class="closeModal" @click="postInventoryCancel">
            ×
        </div>
    </modal>
</div>
</template>

<script>
import {
    inventoryMixin
} from "../mixins/inventoryMixin";
import {
    urlParameterMixin
} from "../mixins/urlParameterMixin";

export default {
    mixins: [inventoryMixin, urlParameterMixin],
    data() {
        return {
            isInvalidFormat: false,
            prevScreenName: ''
        }
    },
    mounted() {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem("organizationId");
        this.mlComponentId = sessionStorage.getItem("mlComponentId");
        this.getMLComponent();
        this.getDataTypes();
        this.getFileSystems();
    },
    methods: {
        show(prevScreenName, selectDataType, selectedFormats) {
            this.clearInputInventory();
            this.$modal.show("inventoryAddModal");
            this.selectDataType = selectDataType;
            this.selectedType = selectDataType;
            this.selectedFormats = selectedFormats
            this.changeFormatTypeList()
            this.prevScreenName = prevScreenName;
        },
        hide() {
            this.clearInputInventory();
            this.$modal.hide("inventoryAddModal");
        },
        postInventory() {
            this.errorMessages = [];
            this.commonCheckInventory();
            if (this.errorMessages.length === 0) {
                if (confirm(this.$t("confirm.create"))) {
                    this.setInventory();
                    this.requestData.Formats = [this.selectedFormats];
                    this.requestData.DataTypeId = undefined;
                    const url = this.$backendURL +
                        "/" +
                        this.organizationIdCheck +
                        "/mlComponents/" +
                        this.mlComponentId +
                        "/inventories"
                    this.$axios.post(url, this.requestData)
                        .then((response) => {
                            this.result = response.data;
                            this.$emit("addInventory");
                            this.clearInputInventory();
                            this.hide();
                        })
                        .catch((error) => {
                            if (this.checkAndWarnInventoryError(error.response.data)){
                                return;
                            }
                            this.$router.push({
                                name: "Information",
                                params: {
                                    error
                                }
                            })
                        })
                }
            } else {
                scrollTo(0, 0);
            }
        },
        postInventoryCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.hide();
            }
        },
        clearInputInventory(){
            this.name = "";
            this.filePath = "";
            this.selectedFileSystem = "";
            this.description = "";
            this.isInvalidFormat = false;
            this.errorMessages = [];
        }
    },
};
</script>

<style scoped>
.inventory-body {
    padding-bottom: 20px;
    width: 550px;
    border: 1px solid #333333;
    border-radius: 10px;
    margin: auto;
}

.template-button {
    padding: 5px;
    margin: 20px;
}

.column {
    display: inline-block;
    width: 5em;
    text-align: left;
}

.column-description {
    display: flex;
    text-align: left;
    margin-left: 10px;
}

.formatError {
    position: absolute;
    left: 480px;
    top: 70px;
    font-size: 14px;
    font-weight: bold;
    color: #ff0000;
}

.column-format {
    display: flex;
    text-align: left;
    margin-left: 10px;
}

.formats {
    display: flex;
    text-align: left;
    margin-left: 120px;
}

.column-formatType {
    display: flex;
    text-align: left;
    margin-left: 50px;
}

.template-hr {
    border-bottom: solid lightgray;
}

.error-message {
    font-weight: bold;
    color: #ff0000;
}

.formCreate {
    position: relative;
    top: 10px;
}

.modalContents>>>.vm--modal {
    text-align: left;
    position: absolute !important;
    top: 10% !important;
    left: 22% !important;
    width: 733px !important;
    height: auto !important;
    padding: 15px 30px !important;
    background-color: #f0f0f0;
}

.modalContents {
    overflow-y: auto;
    max-width: 100%;
}

.modalContents dt {
    width: 200px;
    /*ラベルの幅 文字数に合わせる*/
    margin-left: 50px;
    /*ラベルの位置 テーブルやリストに合わせる*/
    float: left;
}

.modalContents span {
    margin-left: 20px;
}

.modalContents dl {
    margin-bottom: 15px;
}

.modalContents .margin {
    text-align: left;
    margin-left: 50px;
    margin-bottom: 0px;
}

#openModal {
    position: relative;
    top: 52px;
    right: 24px;
    z-index: 1;
}

#btn_set {
    margin-bottom: 10px;
}
</style>
