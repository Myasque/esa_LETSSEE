plugins {
    alias(libs.plugins.androidApplication)
}

android {
    namespace = "com.example.galileomastermindboilerplate"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.galileomastermindboilerplate"
        minSdk = 28
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    buildFeatures {
        viewBinding = true
    }
}

dependencies {

    implementation(libs.appcompat)
    implementation(libs.material)
    implementation(libs.constraintlayout)
    implementation(libs.lifecycle.livedata.ktx)
    implementation(libs.lifecycle.viewmodel.ktx)
    implementation(libs.navigation.fragment)
    implementation(libs.navigation.ui)
    testImplementation(libs.junit)
    androidTestImplementation(libs.ext.junit)
    androidTestImplementation(libs.espresso.core)
    // add by mingyu 4/5 1017
    implementation("com.squareup.okhttp3:okhttp:4.9.0")
   // implementation("com.google.android.gms:play-services-location:16.0.0")
   // implementation("com.google.guava:guava:16+")

}


