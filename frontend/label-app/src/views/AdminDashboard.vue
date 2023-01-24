<template>
<section class="ftco-section">
    <div class="container add">
        <div class="row top-bar">
            <div class="col-md-9 mb-8">
                <h1 class="heading-section">Welcome {{ store.email }}!</h1>
                <p>Institution: {{ store.institution }}</p>
            </div>
            <div class="col-md-3 mb-2">
                <button @click="logout" type="submit" class="form-control btn btn-dark submit px-3 logout-button mt-3">
                    Logout
                </button>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-12">
                <div class="wrap d-md-flex">
                    <div class="login-wrap p-4 p-lg-5 col-md-12 col-lg-12">
                        <div class="d-flex">
                            <div class="w-100">
                                <h4 class="mb-4">Databases</h4>
                            </div>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col-md-12 col-lg-12">
                                <div class="wrap p-1 p-lg-1">
                                    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link active" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">Add Database</button>
                                        </li>
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" aria-selected="false">Add Claims</button>
                                        </li>
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link" id="pills-contact-tab" data-bs-toggle="pill" data-bs-target="#pills-contact" type="button" role="tab" aria-controls="pills-contact" aria-selected="false">Others</button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="tab-content" id="pills-tabContent">
                            <div class="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab">
                                <div class="row justify-content-center">
                                    <div class="col-md-12 col-lg-12">
                                        <div class="wrap d-md-flex">
                                            <div class="text-wrap p-4 p-lg-5 text-center d-flex order-md-last">
                                                <div class="text w-100">
                                                    <div class="text w-100 list-database overflow-auto">
                                                        <h4 class="view-database-label">Databases</h4>
                                                        <ol class="list-group list-group-numbered">
                                                            <transition-group name="listtransition">
                                                                <template v-for="item in returnData" :key="item.id">
                                                                    <li class="list-group-item d-flex justify-content-between align-items-start">
                                                                        <div class="ms-2 me-auto w-80">
                                                                            <div class="fw-bold">{{ item.name }}</div>
                                                                            {{ item.description }}
                                                                            <div>
                                                                                <span class="numberClaims">{{ item.num_claims }} claims</span>
                                                                            </div>
                                                                            <div class="fw-bold">
                                                                                <span v-if="item.is_active == true" class="badge bg-primary rounded-pill">Active</span>
                                                                                <span v-else="item.is_active == false" class="badge bg-primary rounded-pill">Not Active</span>
                                                                            </div>
                                                                        </div>
                                                                        <div class="options w-40">
                                                                            <button v-if="item.is_active == false" class="btn btn-success delete-button" value=True @click="activateDatabase" :id="'activate-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Activate
                                                                            </button>
                                                                            <button v-else="item.is_active == true" class="btn btn-danger delete-button" value=False @click="activateDatabase" :id="'activate-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Deactivate
                                                                            </button>
                                                                            <button class="btn btn-primary delete-button" @click="deleteDatabase" :id="'delete-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Delete
                                                                            </button>
                                                                        </div>
                                                                    </li>
                                                                </template>
                                                            </transition-group>
                                                        </ol>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="login-wrap p-4 p-lg-5">
                                                <form @submit.prevent="mainAddDatabase" class="add-database-form">
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="name">Name of database</label>
                                                        <input type="text" v-model="databaseName" class="form-control" placeholder="Database Name" required>
                                                    </div>
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="name">Short Description</label>
                                                        <input type="text" v-model="description" class="form-control" placeholder="Write a short description." required>
                                                    </div>
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="password">Database Password</label>
                                                        <input type="password" v-model="databasePassword" class="form-control" placeholder="Password" :maxlength="20" required>
                                                        <div class="password_validation" v-text="(20 - databasePassword.length) + ' chars left'"></div>
                                                    </div>
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="password">Temporal Dataset</label>
                                                        <div class="form-check form-switch">
                                                            <input class="form-check-input form-control" v-model="isTemporal" type="checkbox" value="true" role="switch" id="flexSwitchCheckChecked">
                                                            <label class="form-check-label" for="flexSwitchCheckChecked">Check for temporal dataset</label>
                                                        </div>
                                                    </div>
                                                    <div class="form-group mb-3 upload">
                                                        <label class="label" for="password">Upload Claims and Evidences</label>
                                                        <file-pond name="uploadFile" ref="pond" class="upload-file" class-name="upload-file" credits="false" label-idle="Drop files here..." allow-multiple="true" required="true" maxFiles=3 accepted-file-types="application/json" v-bind:files="uploadedFiles" v-on:init="handleFilePondInit" />
                                                    </div>
                                                    <div class="form-group">
                                                        <button type="submit" class="form-control btn btn-primary submit px-3">Add Database</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab">
                                <div class="row justify-content-center">
                                    <div class="col-md-12 col-lg-12">
                                        <div class="wrap d-md-flex">
                                            <div class="text-wrap p-4 p-lg-5 text-center d-flex order-md-last">
                                                <div class="text w-100">
                                                    <div class="text w-100 list-database overflow-auto">
                                                        <h4 class="view-database-label">Claims</h4>
                                                        <ol class="list-group list-group-numbered">
                                                            <transition-group name="listtransition">
                                                                <template v-for="item in claimData" :key="item.id">
                                                                    <li class="list-group-item d-flex justify-content-between align-items-start">
                                                                        <div class="ms-2 me-auto w-80">
                                                                            <div class="fw-bold">{{ item.content }}</div>
                                                                            <div class="fw-bold">
                                                                                <span class="badge bg-primary rounded-pill">Initial Label: {{ item.initial_label }}</span>
                                                                            </div>
                                                                        </div>
                                                                        <div class="options w-40">
                                                                            <button class="btn btn-primary delete-button" @click="deleteClaim" :id="'delete-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Delete
                                                                            </button>
                                                                        </div>
                                                                    </li>
                                                                </template>
                                                            </transition-group>
                                                        </ol>
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- Add Evidence Modal -->
                                            <div class="modal fade" id="evidenceModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Add evidence</h1>
                                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <form @submit.prevent="addEvidenceConfirm" class="add-evidence-form">
                                                            <div class="modal-body">
                                                                <div class="form-group mb-3">
                                                                    <label class="label" for="name">Evidence Title</label>
                                                                    <input type="text" ref="titleField" class="form-control" placeholder="Evidence title." required>
                                                                </div>
                                                                <div class="form-group mb-3">
                                                                    <label class="label" for="password">Evidence Content</label>
                                                                    <input type="text" ref="evidenceField" class="form-control" placeholder="Evidence Content" required>
                                                                </div>
                                                                <div class="form-group mb-3">
                                                                    <label class="label" for="password">Evidence Tag</label>
                                                                    <select class="form-select" ref="evidenceInitialTagField" aria-label="Evidence select initial tag" required>
                                                                        <option selected>Choose one from the menu:</option>
                                                                        <option value="SUPPORTS">Supports</option>
                                                                        <option value="REFUTES">Refutes</option>
                                                                        <option value="NOT ENOUGH INFORMATION">Not enough Information</option>
                                                                    </select>
                                                                </div>
                                                            </div>
                                                            <div class="modal-footer">
                                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                                <button class="btn btn-primary addEvidenceButton" data-bs-dismiss="modal">Add evidence</button>
                                                            </div>
                                                        </form>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="login-wrap p-4 p-lg-5">
                                                <form @submit.prevent="addClaimAndEvidenceManual">
                                                    <div class="form-group">
                                                        <label class="label" for="name">Select a database</label>
                                                        <div class="databaseDropdown">
                                                            <button class="btn btn-secondary dropdown-toggle" type="button" ref="selectDatabaseBtn" data-bs-toggle="dropdown" aria-expanded="false">
                                                                Select a Database
                                                            </button>
                                                            <ul class="dropdown-menu" aria-labelledby="selectDatabase">
                                                                <template v-for="item in returnData" :key="item.id">
                                                                    <li value="item.id">
                                                                        <a class="dropdown-item" v-on:click="changeSelectedDatabase(item.id, item.name)">{{ item.id }} - {{ item.name }}</a>
                                                                    </li>
                                                                </template>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                    <div class="form-check form-switch form-switch-lg">
                                                        <input class="form-check-input addClaimsViaUpload" type="checkbox" v-model="uploadFiles" role="switch" id="flexSwitchCheckDefault">
                                                        <label class="form-check-label" for="flexSwitchCheckDefault">Check to upload files instead</label>
                                                    </div>
                                                    <template v-if="!uploadFiles">
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="name">Claim</label>
                                                            <input type="text" v-model="addClaimContent" class="form-control" placeholder="Claim content." required>
                                                        </div>
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="password">Original ID</label>
                                                            <input type="number" v-model="addClaimOriginalID" class="form-control" placeholder="Original ID" required>
                                                        </div>
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="password">Initial Label</label>
                                                            <select class="form-select" aria-label="Default select example" v-model="selectedInitialLabel" required>
                                                                <option selected>Choose one from the menu:</option>
                                                                <option value="SUPPORTS">Supports</option>
                                                                <option value="REFUTES">Refutes</option>
                                                                <option value="NOT ENOUGH INFORMATION">Not enough Information</option>
                                                            </select>
                                                        </div>
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="password">Train / Test </label>
                                                            <select class="form-select" aria-label="Default select example" v-model="selectedTrainLabel" required>
                                                                <option selected>Choose one from the menu:</option>
                                                                <option value=1>Train</option>
                                                                <option value=0>Test</option>
                                                            </select>
                                                        </div>
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="password">Add Evidence</label>
                                                            <button class="btn btn-secondary px-3 ml-4" data-bs-toggle="modal" data-bs-target="#evidenceModal">Add Evidence</button>
                                                            <div v-if="addEvidenceStore.length != 0" class="evidences overflow-auto">
                                                                <ol class="list-group list-group-numbered">
                                                                    <template v-for="(evidence, index) in addEvidenceStore" :key="index">
                                                                        <li class="list-group-item d-flex justify-content-between align-items-start">
                                                                            <div class="ms-2 me-auto w-80">
                                                                                <div class="fw-bold">{{ addEvidenceTitle[index] }}</div>
                                                                                {{ evidence }}
                                                                                <div class="fw-bold">
                                                                                    <span class="badge bg-primary rounded-pill">Initial Label: {{ addEvidenceLabel[index] }}</span>
                                                                                </div>
                                                                            </div>
                                                                            <div class="options w-40">
                                                                                <button @click="deleteEvidenceConfirm" class="btn btn-primary delete-button px-1" :id="'delete-' + index" style="--bs-btn-font-size: 0.9rem;" type="button">
                                                                                    Remove Evidence
                                                                                </button>
                                                                            </div>
                                                                        </li>
                                                                    </template>
                                                                </ol>
                                                            </div>
                                                            <div v-else class="mt-2">
                                                                <p>No evidence added yet.</p>
                                                            </div>
                                                        </div>
                                                    </template>
                                                    <template v-else="!uploadFiles">
                                                        <div class="form-group mb-3 upload">
                                                            <label class="label" for="password">Upload Claims and Evidences</label>
                                                            <file-pond name="uploadFilesManual" ref="manualpond" class="upload-file" class-name="upload-file" credits="false" label-idle="Drop files here..." allow-multiple="true" required="true" maxFiles=3 accepted-file-types="application/json" v-bind:files="uploadedFilesManual" v-on:init="handleFilePondInit" />
                                                        </div>
                                                    </template>
                                                    <div class="form-group">
                                                        <button class="form-control btn btn-primary submit px-3">Add Claims</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="pills-contact" role="tabpanel" aria-labelledby="pills-contact-tab">1</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-12">
                <div class="wrap d-md-flex">
                    <div class="login-wrap p-4 p-lg-5 col-md-12 col-lg-12">
                        <div class="d-flex">
                            <div class="w-100">
                                <h4 class="mb-4">Annotation</h4>
                            </div>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col-md-12 col-lg-12">
                                <div class="wrap p-1 p-lg-1">
                                    <ul class="nav nav-pills mb-3" id="pills-tab-annotation" role="tablist">
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link active" id="pills-annotation-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">Generate Annotation Results</button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="tab-content" id="pills-tabContent">
                            <div class="tab-pane fade show active" id="pills-annotation" role="tabpanel" aria-labelledby="pills-annotation-tab">
                                <div class="row justify-content-center">
                                    <div class="col-md-12 col-lg-12">
                                        <div class="col-md-12 col-lg-12 login-wrap p-4 p-lg-5">
                                            <div class="form-group">
                                                <label class="label" for="name">Select a database</label>
                                                <div class="databaseDropdown">
                                                    <button class="btn btn-secondary dropdown-toggle" type="button" ref="selectDatabaseBtnAnnotation" data-bs-toggle="dropdown" aria-expanded="false">
                                                        Select a Database
                                                    </button>
                                                    <ul class="dropdown-menu" aria-labelledby="selectDatabase">
                                                        <template v-for="item in returnData" :key="item.id">
                                                            <li value="item.id">
                                                                <a class="dropdown-item" v-on:click="changeSelectedDatabaseAnnotation(item.id, item.name)">{{ item.id }} - {{ item.name }}</a>
                                                            </li>
                                                        </template>
                                                    </ul>
                                                </div>
                                                <div class="form-group mt-3">
                                                    <button type="submit" @click=getAnnotations class="form-control btn btn-primary submit px-3">Download Annotation Results</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<template v-if="showModal">
    <div class="modal show" id="dashboardModal" style="display: block;">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" v-if="loadingAdd" id="dashboardModalLabel">Loading</h1>
                    <h1 class="modal-title fs-5" v-else id="dashboardModalLabel">Operation Completed</h1>
                    <button type="button" class="btn-close" v-if="loadingAdd == false" @click=clearModalMessage></button>
                </div>
                <div class="modal-body">
                    <h4></h4>
                    <div class="text w-100 list-database overflow-auto model-message">
                        <h6><strong>{{ claimNumber }}</strong> claims added in total.</h6>
                        <h6><strong>{{ evidenceNumber }}</strong> evidences added in total.</h6>
                        <template v-if="loadingAdd">
                            <div class="spinner-grow text-secondary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span> Adding claims ... Please be patient.</span>
                        </template>
                        <ol class="list-group list-group-numbered" id="modelMessage">
                            <hr />
                            <h6><strong>Log: </strong></h6>
                            <template v-for="item in modalMessages">
                                <li class="message-list d-flex">
                                    <p>{{ item }}</p>
                                </li>
                            </template>
                        </ol>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" @click=clearModalMessage v-if="loadingAdd" class="btn btn-secondary" disabled>Close</button>
                    <button type="button" @click=clearModalMessage v-else class="btn btn-secondary">Close</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal-backdrop show"></div>
</template>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { useVuelidate } from '@vuelidate/core';
import { useToast } from "vue-toastification";
// Import FilePond
import vueFilePond from 'vue-filepond';
// Import plugins
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js';
// Import styles
import 'filepond/dist/filepond.min.css';
// Create FilePond component
const FilePond = vueFilePond(FilePondPluginFileValidateType);

export default {
    setup() {
        // Get toast interface
        const toast = useToast();
        // Set up Pinia User store
        const store = useUserStore();
        const token = store.token;
        if (token) {
            axios.defaults.headers.common['Authorization'] = "Token " + token
        } else {
            axios.defaults.headers.common['Authorization'] = ""
        }
        return { store, toast, v$: useVuelidate(), }
    },
    mounted() {
        this.getDatabases();
    },
    name: 'AdminDashboard',
    data() {
        return {
            uploadedFiles: [],
            databaseName: "",
            description: "",
            databasePassword: "",
            isTemporal: false,
            returnData: null,
            claimData: null,

            loadingAdd: false,
            fileReadObject: null,

            selectedDatabase: "",
            modeForClaims: "",

            uploadFiles: false,
            addClaimContent: "",
            addClaimOriginalID: "",
            selectedInitialLabel: "",
            selectedTrainLabel: null,

            uploadedFilesManual: [],
            addEvidenceStore: [],
            addEvidenceTitle: [],
            addEvidenceLabel: [],

            modalMessages: [],
            claimNumber: 0,
            evidenceNumber: 0,
            showModal: false,

            selectedDatabaseAnnotation: "",

        };
    },
    methods: {
        logout() {
            const store = useUserStore();
            store.removeToken()
            this.$router.push('/')
        },
        // Generates a random salt for database password
        generateRandomSalt() {
            let result = ' ';
            for (let i = 0; i < length; i++) {
                result += characters.charAt(Math.floor(Math.random() * 20));
            }
            return result;
        },
        reshuffle: function shuffle(array) {
            let currentIndex = array.length,
                randomIndex;

            // While there remain elements to shuffle.
            while (currentIndex != 0) {

                // Pick a remaining element.
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;

                // And swap it with the current element.
                [array[currentIndex], array[randomIndex]] = [
                    array[randomIndex], array[currentIndex]
                ];
            }

            return array;
        },
        handleFilePondInit: function () {
            console.log('FilePond has initialized');
        },
        clearModalMessage() {
            this.modalMessages = [];
            this.showModal = false;
            this.claimNumber = 0;
            this.evidenceNumber = 0;
            this.getDatabases();
            if (this.selectedDatabase != "") {
                this.getClaims(this.selectedDatabase)
            }
        },
        mainAddDatabase(e) {
            const pondFiles = this.$refs.pond.getFiles();
            this.addDatabase(e, pondFiles, "")
        },
        async addDatabase(e, pondFiles, databaseID) {
            // Show the loading modal to indicate progress
            this.loadingAdd = true;
            this.showModal = true;
            // If there is json formatting issues, do not process that claim
            for (var i = 0; i < pondFiles.length; i++) {
                const fileLoad = await new Promise(resolve => {
                    this.fileReadObject = null;
                    const fileName = pondFiles[i].filename
                    const fr = new FileReader();
                    fr.readAsText(pondFiles[i].file);
                    var self = this;
                    fr.onload = async (e) => {
                        let text = e.target.result
                        try {
                            let result = text.split('\n').map(function (record) {
                                if (record != "") {
                                    return JSON.parse(record)
                                }
                            })
                            // Remove empty strings from list
                            self.fileReadObject = result.filter(item => item);
                        } catch (e) {
                            self.toast.error("Please check the json formatting in the file named: " + fileName);
                            return
                        }

                        let lengthResult = self.fileReadObject.length
                        let trainSize = Math.ceil(0.7 * lengthResult)
                        let testSize = lengthResult - trainSize
                        let trainTestSplit = new Array(trainSize).fill(1);
                        if (testSize > 0) {
                            let testArray = new Array(lengthResult - trainSize).fill(0);
                            trainTestSplit = self.reshuffle(trainTestSplit.concat(testArray));
                        }

                        for (let j = 0; j < self.fileReadObject.length; j++) {
                            let obj = self.fileReadObject[j];
                            // Add main database in via axios, only if json formatting is correct
                            var evidence_headers = ['evidence_title', 'evidence_content']
                            var evidence = obj.evidence.map(function (a) {
                                var object = {};
                                evidence_headers.forEach(function (k, i) {
                                    object[k] = a[i];
                                });
                                return object;
                            });
                            var newFlag = true;
                            if (databaseID != "") {
                                newFlag = false;
                            }
                            const sendData = {
                                new: newFlag,
                                // Database
                                owner: self.store.userid,
                                name: self.databaseName,
                                databaseId: databaseID,
                                description: self.description,
                                accesskey: self.databasePassword,
                                is_temporal: self.isTemporal,
                                salt: self.generateRandomSalt(),
                                // Claim
                                claimContent: obj.claim,
                                original_id: obj.id,
                                initial_label: obj.label,
                                train_test_label: parseInt(trainTestSplit[j]),
                                // Temporal
                                temporalContent: JSON.stringify(obj.claim_temporal_arguments),
                                // Evidence
                                evidence: JSON.stringify(evidence),
                                // Golden Evi
                                golden_evi: JSON.stringify(obj.golden_evi),
                            }

                            // We want to do this sequentially first, since chrome cannot send too many parallel Axios requests

                            const axiosResult = await axios
                                .post('/api/v1/database/newdb/', sendData)
                                .then(response => {
                                    self.claimNumber = self.claimNumber + 1;
                                    self.evidenceNumber = self.evidenceNumber + response.data.numEvidence;
                                })
                                .catch(error => {
                                    // Request was made and server responded unfavourably
                                    if (error.response.data.non_field_errors[0]) {
                                        self.toast.error(error.response.data.non_field_errors[0]);
                                    }
                                    // Request was made but no response received
                                    else if (error.request) {
                                        self.toast.error("Received no response from the server. Please try again.");
                                    }
                                    // Something else happened
                                    else {
                                        self.toast.error("Sorry, an unknown error occurred. Please try again.");
                                    }
                                })
                        }
                        resolve()
                    }
                });
            }
            this.loadingAdd = false;
        },
        async addClaimAndEvidenceManual(e) {
            const databaseId = this.selectedDatabase;

            if (this.uploadFiles) {
                const manualPondFiles = this.$refs.manualpond.getFiles();
                const added = await this.addDatabase(e, manualPondFiles, databaseId)
            } else {
                const claim = this.addClaimContent;
                const claimId = this.addClaimOriginalID;
                const claimLabel = this.selectedInitialLabel;
                const trainLabel = this.selectedTrainLabel;
                const temporalSections = [];
                const evidences = this.addEvidenceTitle.map((e, i) => [e, this.addEvidenceStore[i]]);
                this.addClaims(databaseId, claim, claimId, claimLabel, evidences, temporalSections, this.addEvidenceLabel, trainLabel);
                this.toast.success("Claims and evidences added successfully.");
            }
        },
        addClaims(databaseId, claim, claimId, claimLabel, evidences, temporalSections, golden_evi, trainTest) {
            const claimData = {
                database: databaseId,
                content: claim,
                original_id: claimId,
                initial_label: claimLabel,
                train_test_label: parseInt(trainTest),
            }
            axios
                .post('/api/v1/database/claims/create/', claimData)
                .then(response => {
                    this.modalMessages.push("Successfully added claim: \"" + claim + "\" to database.")
                    // Add temporal section
                    for (let k = 0; k < temporalSections.length; k++) {
                        this.addTemporalArguments(response.data.id, temporalSections[k]);
                    }

                    //Add evidences
                    for (let k = 0; k < evidences.length; k++) {
                        this.addEvidence(response.data.id, evidences[k][0], evidences[k][1], golden_evi[k]);
                    }

                    this.getClaims(this.selectedDatabase)
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        addTemporalArguments(claimId, temporalContent) {
            const temporalData = {
                claim: claimId,
                content: temporalContent,
            }
            axios
                .post('/api/v1/database/temporalargs/create/', temporalData)
                .then(response => {
                    if (response.data.created == false) {
                        this.modalMessages.push("Temporal Argument - " + temporalContent + " already exists for this claim. The temporal argument will not be added.")
                    } else {
                        this.modalMessages.push("Successfully added temporal argument - " + temporalContent + " to database.")
                    }
                })
                .catch(error => {
                    console.log(error)
                    this.modalMessages.push("There were some issues adding Temporal Argument - " + temporalContent + " .");
                })
        },
        // Main evidence add on database add page
        addEvidence(claimId, title, content, golden_evi) {
            const evidenceData = {
                claim: claimId,
                title: title,
                content: content,
                golden_evi: golden_evi,
            }
            console.log(evidenceData)
            axios
                .post('/api/v1/database/evidence/create/', evidenceData)
                .then(response => {
                    if (response.data.created == false) {
                        this.modalMessages.push("Evidence - " + content + " already exists. The evidence will not be added.")
                    } else {
                        this.evidenceNumber = this.evidenceNumber + 1;
                        this.modalMessages.push("Successfully added evidence - " + content + " to database.")
                    }
                    // Successfully added database, claims and evidences
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    this.modalMessages.push("There were some issues adding evidence - " + content + " .");
                })

        },
        getDatabases() {
            axios
                .get('/api/v1/database/')
                .then((response) => {
                    this.returnData = response.data
                    console.log(this.returnData)
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    this.toast.error("There was some issue retrieving databases.");
                })
        },
        activateDatabase: function (e) {
            console.log(e.target.id.substring(9))
            const updatedData = {
                is_active: e.target.value,
            }
            axios
                .patch('/api/v1/database/update/' + e.target.id.substring(9) + '/', updatedData)
                .then((response) => {
                    console.log(response.data)
                    this.getDatabases()
                    if (updatedData.is_active == "True") {
                        this.toast.success("Database is activated and ready for labelling.");
                    } else {
                        this.toast.success("Database is deactivated and labelling cannot be done.");
                    }
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        deleteDatabase: function (e) {
            axios
                .delete('/api/v1/database/delete/' + e.target.id.substring(7) + '/')
                .then((response) => {
                    console.log(response.data)
                    this.getDatabases()
                    this.toast.success("Database is successfully deleted.");
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        changeSelectedDatabase(id, name) {
            this.selectedDatabase = id;
            this.$refs.selectDatabaseBtn.innerText = id + " - " + name;
            // Updates claims as well
            this.getClaims(this.selectedDatabase);
        },
        changeSelectedDatabaseAnnotation(id, name) {
            this.selectedDatabaseAnnotation = id;
            this.$refs.selectDatabaseBtnAnnotation.innerText = id + " - " + name;
        },
        getClaims(dbId) {
            axios
                .get('/api/v1/database/claims/list/', {
                    params: { databaseId: dbId }
                })
                .then((response) => {
                    console.log(response.data)
                    this.claimData = response.data
                    console.log(this.claimData)
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        // Delete claims
        deleteClaim: function (e) {
            axios
                .delete('/api/v1/database/claims/delete/' + e.target.id.substring(7) + '/')
                .then((response) => {
                    console.log(response.data)
                    this.getClaims(this.selectedDatabase)
                    this.toast.success("Claim is successfully deleted.");
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        // Manual add evidence on add claims page to append to internal data lists
        addEvidenceConfirm() {
            this.addEvidenceTitle.push(this.$refs.titleField.value)
            this.addEvidenceStore.push(this.$refs.evidenceField.value)
            this.addEvidenceLabel.push(this.$refs.evidenceInitialTagField.value)
        },
        deleteEvidenceConfirm: function (e) {
            const indexToDelete = e.target.id.substring(7)
            this.addEvidenceTitle.splice(indexToDelete, 1)
            this.addEvidenceStore.splice(indexToDelete, 1)
            this.addEvidenceLabel.splice(indexToDelete, 1)
        },
        getAnnotations() {
            axios
                .get('/api/v1/database/annotation/list/', {
                    params: { databaseId: this.selectedDatabaseAnnotation }
                })
                .then((response) => {
                    console.log(JSON.stringify(response.data))
                    var bb = new Blob([JSON.stringify(response.data)], { type: 'text/json' });
                    var a = document.createElement('a');
                    a.download = 'annotation_results.json';
                    a.href = window.URL.createObjectURL(bb);
                    a.click();
                    a.remove();
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
    },
    components: {
        FilePond,
    },
}
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css");

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.upload {
    margin-top: 30px;
}

.form-check-label {
    margin-left: 15px;
    margin-top: 10px;
}

#flexSwitchCheckChecked {
    width: 40px;
    height: 40px;
}

.password_validation {
    margin-top: 15px;
}

.view-database-label {
    padding-top: 10px;
    margin-bottom: 10px;
}

.list-database {
    height: 600px;
    background-color: white;
    border-radius: 5px;
}

.list-group-item {
    background-color: #faf5f5;
    margin-bottom: 5px;
}

.options {
    margin-top: auto;
    margin-bottom: auto;
}

.delete-button {
    margin-left: 10px;
}

.listtransition-enter-active,
.listtransition-leave-active {
    transition: all 1s;
}

.listtransition-enter,
.listtransition-leave-to {
    opacity: 0;
    transform: translateX(-295px);
}

.form-switch.form-switch-lg {
    margin-bottom: 1.5rem;
    /* JUST FOR STYLING PURPOSE */
    width: 100%;
}

.form-switch.form-switch-lg .form-check-input {
    height: 2rem;
    width: calc(3rem + 0.75rem);
    border-radius: 4rem;
}

.form-check-label {
    margin-left: 30px;
}

.evidences {
    margin-top: 20px;
    width: 100%;
    height: 200px;
    border: 1px solid rgb(210, 210, 210);
}

.model-message {
    height: 300px;
    background-color: #f5f2f2;
    padding: 10px;
    border-radius: 5px;
}

.message-list {
    border-radius: 5px;
    background-color: white;
    border: 1px #c2c0c0 solid;
    padding: 5px;
    margin-top: 5px;
}

.numberClaims {
    font-size: 14px;
    font-weight: 600;
}

.logout-button {
    width: 200px;
}

/* @import '../assets/css/homepage.css'; */
</style>
